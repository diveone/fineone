import os, sys, tempfile
import requests, requests_mock
import pytest
from flask_sqlalchemy import SQLAlchemy

from config import testing
from finone import app, create_app
from finone.api import ApiRequest, ApiResponse
from finone.factories import RateQuoteFactory, RequestFactory


db = SQLAlchemy()

@pytest.fixture
def params():
    data = {
        "state": "CA",
        "county": "Alameda",
        "loanAmount": 300000,
        "propertyType": "single_family",
        "loanPurpose": 'purchase',
        "appraisedValue": 600000,
        'zipcode': '94619'
    }
    return data


@pytest.fixture(scope="module")
def client():
    app.testing = True
    _app = app.test_client()

    return _app


@pytest.fixture
def test_app():
    _app = create_app(db, testing)
    _app.testing = True

    return _app


class TestApiRequest:
    def test_create_request(self, params):
        """Should return request object."""
        api = ApiRequest(params)
        res = api.create_request()
        assert api.loan_amount == 300000
        assert api.state == 'CA'

    @pytest.mark.skip()
    @pytest.mark.usefixtures('test_app')
    def test_send_request_success(self, params):
        api = ApiResponse(params)
        res = api.send_request()
        # assert '200' == api.status_code

