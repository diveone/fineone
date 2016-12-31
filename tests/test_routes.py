import os, sys, tempfile
import requests, requests_mock
import pytest

from finone import app


@pytest.fixture(scope="module")
def client():
    app.testing = True
    _app = app.test_client()

    return _app

@pytest.fixture
def params():
    data = {
        "state": "CA",
        "county": "Alameda",
        "loanAmount": 300000,
        "propertyType": 0,
        "loanpurpose": 1,
        "appraisedValue": 600000,
    }
    return data

class TestRoutes:
    """
    Testing for basic api requests and responses.
    """
    def test_api_status(self, client):
        """Should return 200 OK."""
        response = client.get('/status')
        assert response.status_code == 200

    def test_results_success(self, client, params):
        """Should take form data and return result."""
        response = client.post('/results', data=params)
        assert response.status_code == 200
