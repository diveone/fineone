import logging, os
import requests, xmltodict

from requests import ConnectionError, HTTPError, RequestException, Timeout

from finone import db, app
from finone.mapping import PROPERTY_TYPE_MAP, LOAN_PURPOSE_MAP
from finone.utils import underscoreize
from finone.models import Request, RateQuote
from sqlalchemy.exc import ProgrammingError

class ApiResponse(object):
    def __init__(self, params):
        """
        Takes original request parameters.
        :param params: Data from the submitted form
        """
        params = underscoreize(params)
        self.params = params
        self.status_code = ''

    def create_request(self):
        # TODO: Build property and purpose mappings.
        return {
            "licenseKey": app.config['MORTECH_LICENSEKEY'],
            "thirdPartyName": app.config['MORTECH_THIRDPARTY_NAME'],
            "customerId": app.config['MORTECH_CUSTOMER_ID'],
            "emailAddress": app.config['MORTECH_EMAIL'],
            "request_id": 1,
            "propertyState": self.params['state'],
            "propertyCounty": self.params['county'],
            "loan_amount": self.params['loan_amount'],
            "propertyType": self.get_property_type(),
            "loanpurpose": self.get_loan_purpose(),
            "loanProduct1": '30 year fixed',
            'loanProduct2': '15 year fixed',
            'loanProduct3': '5 year ARM/30 yrs',
            'loanProduct4': '7 year ARM/30 yrs',
            "appraisedvalue": self.params['appraised_value'],
            "targetPrice": '-999',
            "lockindays": '45'
        }

    def get_property_type(self):
        return PROPERTY_TYPE_MAP.get(self.params['property_type'])

    def get_loan_purpose(self):
        return LOAN_PURPOSE_MAP.get(self.params['loan_purpose'])

    def send_request(self):
        """Sends a request to mortech with data."""
        # endpoint = 'http://localhost:5555/test'
        print("Sending request...")

        try:
            data = self.create_request()
            res = requests.get(app.config['LOCAL_ENDPOINT'], params=data)
        except (HTTPError, ConnectionError, Timeout, RequestException, Exception) as exc:
            print(exc)
            app.logger.exception("MORTECH-REQUEST-EXCEPTION: %s", exc)
            self.status_code = '500'
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