import os, sys, tempfile
import requests, requests_mock
import pytest

from finone import app, create_app
from finone.api import ApiResponse
from finone.factories import RateQuoteFactory, RequestFactory
from finone.models import db
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
    _app = create_app(db, 'testing')
    _app.testing = True

    return _app


class TestApi:
    def test_create_request(self, params):
        """Should return request object."""
        api = ApiResponse(params)
        res = api.create_request()
        assert 'loanpurpose' in res

    @pytest.mark.usefixtures('test_app')
    def test_send_request_success(self, params):
        api = ApiResponse(params)
        res = api.send_request()
        assert '200' == api.status_code

