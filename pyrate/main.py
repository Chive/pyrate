import json
import requests
from utils import build_oauth1

__docformat__ = 'sphinx en'


class Pyrate(object):
    """This is the main class

    :param string base_url: The base url for all api requests
    :param default_header_content: Default content for the HTTP request header
    :param default_body_content: Default content for the HTTP request body
    :param dict auth_type: Dictionary with authentification information. Type
    and personal information like api keys or usernames/passwords
    :param bool send_json: Whether the request body should be encoded with json

    :param list response_formats: List of available return formats for this service
    :param string default_response_format: Default return format (will be used if none else is specified in request)
    :param dict connection_check: Used by :func:`check_connection`
    """

    # request
    base_url = None
    default_header_content = None
    default_body_content = None
    auth_data = {'type': None}
    send_json = False

    # response
    response_formats = []
    default_response_format = None
    validate_response = True

    connection_check = {'http_method': None, 'target': None}

    def __init__(self):
        try:
            self.default_response_format = self.response_formats[0]
        except IndexError:
            self.default_response_format = None

    def request(self, method, target, content=None, request_headers=None,
                response_format=None, return_raw=False):

        request_url = '%s%s' % (self.base_url, target)

        if response_format:
            request_url += '.%s' % response_format
        elif self.default_response_format:
            request_url += '.%s' % self.default_response_format

        request_body = dict(self.default_body_content or {}, **(content or {}))
        request_headers = dict(self.default_header_content or {},
                               **(request_headers or {}))
        response_format = '' + ('.' + self.default_response_format if
                                self.default_response_format else '')
        auth_data = self.get_auth_data()

        # TODO: do we really need this?
        if self.send_json:
            # We need to make sure that body is jsonified
            try:
                request_body = json.dumps(request_body)
            except (TypeError, ValueError):
                pass

        response = requests.request(
            method=method, url=request_url, data=request_body,
            headers=request_headers, auth=auth_data)

        if return_raw:
            return response
        else:
            return self.handle_response(response, response_format)

    def delete(self, target, content=None, headers=None, response_format=None, return_raw=False):
        """Sends a DELETE request"""
        return self.request('DELETE', target, content, headers, response_format, return_raw)

    def get(self, target, content=None, headers=None, response_format=None, return_raw=False):
        """Sends a GET request"""
        return self.request('GET', target, content, headers, response_format, return_raw)

    def head(self, target, content=None, headers=None, response_format=None, return_raw=False):
        """Sends a HEAD request"""
        return self.request('HEAD', target, content, headers, response_format, return_raw)

    def options(self, target, content=None, headers=None, response_format=None, return_raw=False):
        """Sends a OPTIONS request"""
        return self.request('OPTIONS', target, content, headers, response_format, return_raw)

    def post(self, target, content=None, headers=None, response_format=None, return_raw=False):
        """Sends a POST request"""
        return self.request('POST', target, content, headers, response_format, return_raw)

    def put(self, target, content=None, headers=None, response_format=None, return_raw=False):
        """Sends a PUT request"""
        return self.request('PUT', target, content, headers, response_format, return_raw)

    def patch(self, target, content=None, headers=None, response_format=None, return_raw=False):
        """Sends a PATCH request"""
        return self.request('PATCH', target, content, headers, response_format, return_raw)

    def handle_response(self, response, response_format):
        if self.check_response(response):
            try:
                return response.json()
            except (ValueError, TypeError):
                return response.content

    def check_response(self, response):
        if self.validate_response and not 200 <= response.status_code < 300:
            raise Exception(
                "There is something wrong with the response (Code: %i)\n"
                "Request was: %s %s\n"
                "Request data was: %s \n"
                "Response Content: %s" % (
                    response.status_code, response.request.method,
                    response.request.url, response.request.body,
                    response.content))
        return True

    def check_connection(self):
        return self.check_response(self.request(
            method=self.connection_check['http_method'],
            target=self.connection_check['target'],
            return_raw=True
        ))

    def get_auth_data(self):
        try:
            auth_type = self.auth_data['type']
        except IndexError:
            return None

        if not auth_type:
            return None

        elif auth_type == 'BASIC':
            return self.auth_data['username'], self.auth_data['password']

        elif auth_type == 'OAUTH1':
            return build_oauth1(
                client_key=self.auth_data['client_key'],
                client_secret=self.auth_data['client_secret'],
                resource_owner_key=self.auth_data['token_key'],
                resource_owner_secret=self.auth_data['token_secret']
            )

        elif auth_type == 'MANUAL':
            return None

        else:
            raise NotImplementedError()

    # Deprecated Methods
    def do(self, *args, **kwargs):
        raise DeprecationWarning("This proxy method is deprecated. Please use "
                                 "the appropriate method directly instead.")
