"""
Flask-Marshmallow (with Flask-SQLAlchemy and marshmallow-sqlalchemy)
https://flask-marshmallow.readthedocs.io/en/latest/
"""
from finone import marshmallow as mm
from finone.models import RateQuote, Request


class RateQuoteSerializer(mm.ModelSchema):
    class Meta:
        model = RateQuote


class RequestSerializer(mm.ModelSchema):
    class Meta:
        model = Request


rate_quotes_serializer = RateQuoteSerializer(many=True)
rate_quote_serializer = RateQuoteSerializer()
request_serializer = RequestSerializer()
