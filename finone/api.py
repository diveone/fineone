import logging
import os
import requests
import xmltodict

from requests import ConnectionError, HTTPError, RequestException, Timeout

from finone import db, app
from finone.constants import (
    PROPERTY_TYPE_MAP, LOAN_PURPOSE_MAP,
    PRODUCT_5_ARM, PRODUCT_7_ARM, PRODUCT_15_FIXED, PRODUCT_30_FIXED,
    ServiceConstants as sc
)
from finone.exceptions import RateQuoteAPIException
from finone.parsers import XmlParser
from finone.utils import underscoreize
from finone.models import Request, RateQuote
from sqlalchemy.exc import ProgrammingError


class ApiRequest(object):
    valid_args = ['state', 'county', 'loan_amount',
                  'appraised_value', 'property_type', 'loan_purpose']

    def __init__(self, params):
        """
        Builds service request object.
        :param params: data from the submitted form
        """
        params = underscoreize(params)
        self.status_code = ''
        # TODO: Figure out what options would possibly be and where to use them
        self.options = {}
        for key, value in params.items():
            if key in valid_args:
                setattr(self, key, value)
            else:
                options.update(key=value)

    def create_request(self):
        return {
            sc.LICENSEKEY: AUTH_LICENSEKEY,
            sc.THIRD_PARTY_NAME: AUTH_NAME,
            sc.CUSTOMER_ID: AUTH_ID,
            sc.EMAIL_ADDRESS: AUTH_EMAIL,
            sc.REQUEST_ID: 1,
            sc.PROPERTY_STATE: self.state,
            sc.PROPERTY_COUNTY: self.county,
            sc.LOAN_AMOUNT: self.loan_amount,
            sc.PROPERTY_TYPE: self.get_property_type(),
            sc.LOAN_PURPOSE: self.get_loan_purpose(),
            sc.LOAN_PRODUCT1: PRODUCT_30_FIXED,
            sc.LOAN_PRODUCT2: PRODUCT_15_FIXED,
            sc.LOAN_PRODUCT3: PRODUCT_5_ARM,
            sc.LOAN_PRODUCT4: PRODUCT_7_ARM,
            sc.APPRAISED_VALUE: self.appraised_value,
            sc.TARGET_PRICE: DEFAULT_TARGET_PRICE,
            sc.LOCKIN_DAYS: DEFAULT_LOCKIN
        }

    def get_property_type(self):
        return PROPERTY_TYPE_MAP.get(self.property_type)

    def get_loan_purpose(self):
        return LOAN_PURPOSE_MAP.get(self.loan_purpose)

    def send_request(self):
        """Sends a request to mortech with data."""
        print("Sending request...")

        try:
            data = self.create_request()
            res = requests.get(app.config['LOCAL_ENDPOINT'], params=data)
        except (HTTPError, ConnectionError, Timeout, RequestException, Exception) as exc:
            app.logger.exception("RQS-REQUEST-EXCEPTION: %s", exc)
            self.status_code = '500'
            raise RateQuoteAPIException(
                exc,
                status=res.status_code,

            )
        else:
            print("Request successful: {0}".format(res.status_code))
            self.status_code = res.status_code
            parser = ApiResponse(res.content, self.request_factory())
            return parser.get_results()

    def request_factory(self):
        data = {
            'property_zipcode': self.params['zipcode'],
            'property_state': self.params['state'],
            'property_type': self.params['property_type'],
            'loan_amount': self.params['loan_amount'],
            'appraised_value': self.params['appraised_value'],
            'loan_purpose': self.params['loan_purpose'],
        }

        req = Request(**data)
        db.session.add(req)
        db.session.commit()
        return req


class ApiResponse(object):
    """
    Manages API responses from Mortech by:

    * Parsing response
    * Storing XML response
    * Storing parsed lenders to database

    Accepts and parses XML responses from the API.

    :param response: XML response from Mortech API
    :param request: An instance of :class:`Request`
    """

    def __init__(self, response, request):
        self.xml = response
        self.data = self.get_data()
        self.request = request

    def is_valid(self):
        return "results" in self.data['mortech']

    def parse(self, data):
        """
        Parses XML to dict. Returns process logs during process.
        To hide these dense logs, move the parsing function to a separate
        method.
        """
        if settings.DEBUG:
            self.save_xml()
        return xmltodict.parse(data)

    def get_data(self):
        """Parses elements of an XML document and returns a list of quotes."""
        return self.parse(self.xml)

    def result_count(self):
        count = 0
        for result in self.data['mortech']['results']:
            count += int(result['@size'])
        service.logger.info("Result count: %s", count)
        return count

    # TODO: abstract method
    def _get_fees(self, fee_list):
        """Accepts list and returns dictionary of fees."""
        fees = {}
        for fee in fee_list:
            fees.update({
                fee.get('@description'): fee.get('@feeamount')
            })
        return fees

    # TODO: abstract method
    def _get_amortization(self, obj):
        """Evaluates presence of intial arm tem to determine amortization."""
        if obj:
            return "Variable"
        else:
            return "Fixed"

    def _get_lenders(self):
        """Return a list of RateQuote instances."""
        lenders = []
        data = self.parse(self.xml)
        results = to_list(data['mortech']['results'])

        for product in results:
            service.logger.info("==> BEGIN: Processing rate quotes for %s products ...",
                                product.get('@product_name'))
            for lender in product['quote']:
                lenders.append(self.lender_factory(lender))
            service.logger.info("==> END: Processing for %s", product.get('@product_name'))
        return lenders

    def bulk_store(self):
        # TODO: Move to ModelManager
        lenders = self._get_lenders()
        service.logger.info("==> BEGIN: Saving lenders ...")
        try:
            db.session.add_all(lenders)
            db.session.commit()
        except (ProgrammingError, Exception) as exc:
            print("BULK STORE EXCEPTION: {}".format(exc))
            raise exc
        else:
            service.logger.info("==> END: %s Lenders saved successfully!", len(lenders))

    def lender_factory(self, lender):
        """Takes a lender Element and parses the attributes."""
        print("Lender Factory - Request ID {}".format(self.request.id))
        data = {
            'request_id': self.request.id,
            'lender_name': lender.get('@vendor_name'),
            'product_description': lender.get('@productDesc'),
            'term': lender.get('@productTerm'),
            'amortization': self._get_amortization(lender.get('@initialArmTerm')),
            'initial_arm': lender.get('@initialArmTerm'),
            'int_only_months': lender.get('@intOnlyMonths'),
            'rate': lender.get('quote_detail').get('@rate'),
            'points': lender.get('quote_detail').get('@price'),
            'origination_fee': lender.get('quote_detail').get('@originationFee'),
            'apr': lender.get('quote_detail').get('@apr'),
            'piti': lender.get('quote_detail').get('@piti'),
            'loan_amount': lender.get('quote_detail').get('@loanAmount'),
            'upfront_fee': lender.get('quote_detail').get('@upfrontFee'),
            'monthly_premium': lender.get('quote_detail').get('@monthlyPremium'),
            'price': lender.get('ratesheet_price'),
            'fees': self._get_fees(lender['quote_detail']['fees']['fee_list']['fee'])
        }
        return RateQuote(**data)

    def save_xml(self):
        """Debug. Stores parsed data to tmp/data."""
        with open('response.xml', 'w+') as doc:
            doc.write(self.xml)

    def get_results(self):
        data = self.get_data()
        self.bulk_store()
        service.logger.info("RESULTS DATA: %s", dict(data['mortech']['header']))

        return to_list(data['mortech']['results'])
