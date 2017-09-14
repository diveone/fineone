"""
Finone API Controller

Processes XML response from Mortech, parses, and stores into database.
Returns response object for user consumption as JSON.
"""
import requests
import xmltodict

from requests import ConnectionError, HTTPError, RequestException, Timeout

from finone import db, app
from finone.constants import (
    AUTH_EMAIL, AUTH_ID, AUTH_LICENSEKEY, AUTH_NAME,
    PROPERTY_TYPE_MAP, LOAN_PURPOSE_MAP,
    PRODUCT_FIXED, PRODUCT_ARM,
    PRODUCT_5_ARM, PRODUCT_7_ARM, PRODUCT_15_FIXED, PRODUCT_30_FIXED,
    DEFAULT_TARGET_PRICE, DEFAULT_LOCKIN,
    ServiceConstants as sc)
from finone.factories import lender_factory, request_factory
from finone.utils import underscoreize
from sqlalchemy.exc import ProgrammingError


class ApiRequest(object):
    """
    Creates and formats a request to the service.
    """

    valid_args = ['state', 'county', 'loan_amount', 'zipcode',
                  'appraised_value', 'property_type', 'loan_purpose']

    def __init__(self, params):
        """
        Builds service request object.
        :param params: data from the submitted form
        """
        self.session = self.create_session()
        params = underscoreize(params)
        self.status_code = ''
        # TODO: Figure out what options would possibly be and where to use them
        self.options = {}
        for key, value in params.items():
            if key in self.valid_args:
                setattr(self, key, value)
            else:
                self.options.update({key: value})

    def _get_property_type(self):
        return PROPERTY_TYPE_MAP.get(self.options.get('property_type'))

    def _get_loan_purpose(self):
        return LOAN_PURPOSE_MAP.get(self.options.get('loan_purpose'))

    def build_request(self):
        return {
            sc.LICENSEKEY: AUTH_LICENSEKEY,
            sc.THIRD_PARTY_NAME: AUTH_NAME,
            sc.CUSTOMER_ID: AUTH_ID,
            sc.EMAIL_ADDRESS: AUTH_EMAIL,
            sc.REQUEST_ID: 1,
            sc.PROPERTY_STATE: self.state,
            sc.PROPERTY_COUNTY: self.county,
            sc.LOAN_AMOUNT: self.loan_amount,
            sc.PROPERTY_TYPE: self._get_property_type(),
            sc.LOAN_PURPOSE: self._get_loan_purpose(),
            sc.LOAN_PRODUCT1: PRODUCT_30_FIXED,
            sc.LOAN_PRODUCT2: PRODUCT_15_FIXED,
            sc.LOAN_PRODUCT3: PRODUCT_5_ARM,
            sc.LOAN_PRODUCT4: PRODUCT_7_ARM,
            sc.APPRAISED_VALUE: self.appraised_value,
            sc.TARGET_PRICE: DEFAULT_TARGET_PRICE,
            sc.LOCKIN_DAYS: DEFAULT_LOCKIN
        }

    @staticmethod
    def create_session():
        """Return an HTTP session."""
        session = requests.Session()
        return session

    def send_request(self):
        """Sends a request to mortech with data."""
        app.logger.info("Sending request...")
        # session = self.create_session()
        try:
            data = self.build_request()
            res = self.session.get(app.config['MORTECH_ENDPOINT'], params=data)
        except (HTTPError, ConnectionError, Timeout, RequestException, Exception) as exc:
            app.logger.exception("RQS-REQUEST-EXCEPTION: %s", exc)
            self.status_code = '500'
            raise
        else:
            app.logger.info("Request successful: {0}".format(res.status_code))
            self.status_code = res.status_code
            parser = ApiResponse(res.content, request_factory())
            return parser.get_results()


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
        if app.debug:
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

    @staticmethod
    def _get_fees(fee_list):
        """Accepts list and returns dictionary of fees."""
        fees = {}
        for fee in fee_list:
            fees.update({
                fee.get('@description'): fee.get('@feeamount')
            })
        return fees

    @staticmethod
    def _get_amortization(obj):
        """Evaluates presence of intial arm tem to determine amortization."""
        if obj:
            return PRODUCT_ARM
        else:
            return PRODUCT_FIXED

    def _get_lenders(self):
        """Return a list of RateQuote instances."""
        lenders = []
        data = self.parse(self.xml)
        results = data['mortech']['results']
        app.logger.info(data.get('mortech').keys())

        for product in results:
            app.logger.info("==> BEGIN: Processing rate quotes for %s products ...",
                            product.get('@product_name'))
            for lender in product['quote']:
                lenders.append(lender_factory(lender))
            app.logger.info("==> END: Processing for %s", product.get('@product_name'))
        return lenders

    def bulk_store(self):
        # TODO: Move to ModelManager
        lenders = self._get_lenders()
        app.logger.info("==> BEGIN: Saving lenders ...")
        try:
            db.session.add_all(lenders)
            db.session.commit()
        except (ProgrammingError, Exception) as exc:
            app.logger.info("BULK STORE EXCEPTION: {}".format(exc))
            raise exc
        else:
            app.logger.info("==> END: %s Lenders saved successfully!", len(lenders))

    def save_xml(self):
        """Debug. Stores parsed data to tmp/data."""
        with open('response.xml', 'w+') as doc:
            doc.write(self.xml)

    def get_results(self):
        data = self.get_data()
        self.bulk_store()
        app.logger.info("RESULTS DATA: %s", dict(data['mortech']['header']))

        return to_list(data['mortech']['results'])


def to_list(data):
    # Move to Utils
    if not isinstance(data, list):
        return [data]
