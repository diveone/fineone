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