import logging
import requests

from flask import abort, jsonify, request, make_response
from flask.views import MethodView
from flask_restful import Resource

from finone import app
from finone.api import ApiRequest
from finone.serializers import (
    rate_quote_serializer,
    rate_quotes_serializer,
    request_serializer)


@app.route('/status')
def api_status():
    """Sends status update for the service."""
    return "Service is available!"


class ApiRequestView(MethodView):

    def post(self):
        """Receives rate quote requests and returns response."""
        response = ApiRequest(request.form)
        app.logger.info('Rate quote request: %s', request.form)
        return jsonify(response.params)

api_request_view = ApiRequestView.as_view('api_request_view')
app.add_url_rule('/results', view_func=api_request_view,
                 methods=['GET', 'POST',])


class RateQuoteResource(Resource):
    def get(self):
        pass
