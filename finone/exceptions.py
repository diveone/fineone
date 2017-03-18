from requests.exceptions import RequestException


class RateQuoteServiceException(Exception):
    def __init__(self, *args, **kwargs):
        if kwargs:
            for key, value in kwargs:
                setattr(self, key, value)


class RateQuoteNetworkException(RateQuoteServiceException):
    """Exceptions for network requests/responses."""
    pass


class RateQuoteAPIException(RateQuoteServiceException):
    """Exceptions for service api."""

    def __init__(self, message, method, status=None, headers=None, network_response=None):
        super(RateQuoteAPIException, self).__init__()
        self.message = message
        self.method = method
        self.status = status
        self.headers = headers
        self.network_response = network_response

    def __unicode__(self):
        return "\nException: {0}\nStatus: {1}\nMethod: {2}\nHeaders: {3}\nNetwork Response:{4}".format(
            self.message,
            self.status,
            self.method,
            self.headers,
            self.network_response
        )
