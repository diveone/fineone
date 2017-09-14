from factory.alchemy import SQLAlchemyModelFactory

from finone.models import db, RateQuote, Request


class RateQuoteFactory(SQLAlchemyModelFactory):
    # TODO: How to get the app name for the session during testing?
    lender = "ABC Mortgage Lending"

    class Meta:
        model = RateQuote
        sqlalchemy_session = db.session


class RequestFactory(SQLAlchemyModelFactory):
    property_state = "California"
    property_county = 'San Francisco'
    property_zipcode = '94111'
    loan_purpose = 'purchase'
    appraised_value = '600000'
    down_payment = '300000'

    class Meta:
        model = Request
        sqlalchemy_session = db.session


def params_factory():
    """Form parameters."""
    return {
        'city': 'Testville',
        'state': 'CA',
        'loanPurpose': 'purchase',
        'loanAmount': '500000',
        'appraisedValue': '700000',
    }


def lender_factory(self, lender):
    """Takes a lender Element and parses the attributes."""
    app.logger.info("Lender Factory - Request ID {}".format(self.request.id))
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


def request_factory(self):
    data = {
        'property_zipcode': self.zipcode,
        'property_state': self.state,
        'property_type': self.property_type,
        'loan_amount': self.loan_amount,
        'appraised_value': self.appraised_value,
        'loan_purpose': self.loan_purpose,
    }

    req = Request(**data)
    db.session.add(req)
    db.session.commit()
    return req