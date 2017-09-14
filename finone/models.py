from flask_sqlalchemy import SQLAlchemy
import shortuuid

from sqlalchemy.orm import relationship
from sqlalchemy import (
    DateTime, func)
from sqlalchemy.types import CHAR, DECIMAL
from sqlalchemy.dialects.postgresql import JSON

db = SQLAlchemy()


# Rename: Lender
class RateQuote(db.Model):
    __tablename__ = 'rate_quotes'

    # FHLMC seems to appear with LP types
    # Agency can occur with FNMA or without
    PRODUCT_TYPE = ['FHA', 'VA', 'Conforming', 'FNMA', 'FHLMC', 'DU']
    AMORTIZATION_TYPE = ['Fixed', 'Variable']
    TERM_TYPE = ['3 Yr', '5 Yr', '7 Yr', '10 Yr', '15 Yr', '30 Yr']

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(22))
    request_id = db.Column(db.Integer, db.ForeignKey('requests.id'))
    created = db.Column(DateTime, default=func.now())  # Also in param lastUpdate
    expiration = db.Column(DateTime)

    lender = db.Column(db.String)
    product_type = db.Column(db.String)     # FHA, Govt, VA, Non-Conforming, Jumbo
    product_name = db.Column(db.String)     # Vendor's name for the product
    description = db.Column(db.String)      # 30 Fixed, 15 ARM, etc
    product_id = db.Column(db.Integer)      # Mortech product ID

    lock_term = db.Column(db.String)        # Lock in days. Default expiration
    term = db.Column(db.String)
    amortization = db.Column(db.String)
    initial_arm = db.Column(db.String)
    rate = db.Column(DECIMAL(6, 3))
    points = db.Column(DECIMAL(6, 3))
    price = db.Column(DECIMAL(6, 3))
    apr = db.Column(DECIMAL(6, 3))
    piti = db.Column(DECIMAL(9, 3))
    loan_amount = db.Column(DECIMAL(12, 3))
    down_payment = db.Column(DECIMAL(12, 3))
    upfront_fee = db.Column(DECIMAL(9, 3))
    origination_fee = db.Column(DECIMAL(9, 3))
    monthly_premium = db.Column(DECIMAL(9, 3))

    fees = db.Column(JSON)
    adjustments = db.Column(JSON)

    request = relationship("Request", back_populates="quotes")

    def __init__(self, *args, **attrs):
        self.uuid = shortuuid.uuid()
        for attr, val in attrs.items():
            setattr(self, attr, val)


# Rename: RateQuoteRequest
class Request(db.Model):
    """
    Request:
    * Identifies every request for RateQuote
    * Related to customer profile if available

    Request is also keyed to the customer profile when
    available.
    """
    LOAN_PURPOSE_OPTIONS = [('purchase', 'Purchase'),
                            ('refi', 'Refinance'),
                            ('cashout', 'Cashout Refinance'),
                            ('both', 'Both')]

    __tablename__ = 'requests'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(CHAR(22))
    customer_id = db.Column(db.Integer)

    # Required parameters sent to generate rate quote results
    property_state = db.Column(db.String)
    property_county = db.Column(db.String)
    property_zipcode = db.Column(db.String)
    loan_purpose = db.Column(db.String)
    appraised_value = db.Column(DECIMAL(12, 3))
    down_payment = db.Column(DECIMAL(12, 3))

    # Relationships: one to many
    quotes = relationship("RateQuote", back_populates="request")

    # User profile fields
    term = db.Column(db.String)
    amortization = db.Column(db.String)
    occupancy = db.Column(db.String)
    property_type = db.Column(db.String)
    credit_score = db.Column(db.String)
    is_veteran = db.Column(db.Boolean)
    motive = db.Column(db.Boolean)          # First time, selling, invest
    loan_timing = db.Column(db.Boolean)     # Now, 3 mos, year
    mortgage_balance = db.Column(DECIMAL(12, 3))
    mortgage_term = db.Column(db.String)
    mortgage_rate = db.Column(db.String)

    def __init__(self, *args, **attrs):
        self.uuid = shortuuid.uuid()
        for k, v in attrs.items():
            setattr(self, k, v)
