from base64 import b64encode
import json
import requests
import sys

__docformat__ = 'restructuredtext en'

class Pyrate(object):
    http_methods = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
    return_formats = ['json']
    default_header_content = None
    default_body_content = None
    default_http_method = None
    default_return_format = None
    connection_check_method = None
    auth_type = None
    base_url = None
    send_json = False

    def __init__(self):
        self.default_http_method = self.http_methods[0]
        try:
            self.default_return_format = self.return_formats[0]
        except IndexError:
            self.default_return_format = ''

    def create_basic_auth(self, user, password):
        # Messing around with Python3's strictness about strings
        """
        Creates the header content for HTTP Basic Authentification
        :param user:
        :param password:
        :return: header content
        """
        if sys.version_info >= (3, 0):
            if not isinstance(user, str):
                user = user.decode('utf-8')

            if not isinstance(password, str):
                password = password.decode('utf-8')

            return 'Basic ' + b64encode((user + ":" + password).encode('utf-8')).decode('utf-8')

        else:
            return 'Basic ' + b64encode(user + ":" + password).rstrip()

    def get_oauth(self):
        raise NotImplementedError("OAuth methods need to be implemented by subclasses!")

    def check_connection(self):
        return self.do(self.connection_check_method[1], http_method=self.connection_check_method[0])

    def build_content(self, args):
         # takes a dictionary, filters out all the empty stuff
        if 'self' in args:
            del args['self']
        new_args = args.copy()

        for key in args:
            if not args[key]:
                del new_args[key]

        return new_args

    def check_response_success(self, response):
        raise NotImplementedError('Please implement in subclass')

    def parse_errors(self, response):
        raise NotImplementedError('Please implement in subclass')

    def do(self, method, content=None, headers=None, http_method=None, return_format=None):

        request_body = self.default_body_content
        if content is not None:
            request_body.update(content)

        request_headers = self.default_header_content
        if headers is not None:
            request_headers.update(headers)

        if http_method is None:
            http_method = self.default_http_method

        if return_format is None:
            if self.default_return_format:
                return_format = "." + self.default_return_format
            else:
                return_format = ''

        request_url = self.base_url + method + return_format

        return self.do_request(http_method, request_url, request_headers, request_body, return_format)

    def do_request(self, http_method, url, headers, body, return_format):

        if self.auth_type == 'OAUTH1':
            auth_data = self.get_oauth()
        else:
            auth_data = None

        if self.send_json:
            # We need to make sure that body is jsonified
            try:
                body = json.dumps(body)
            except TypeError or ValueError:
                pass

        if http_method.upper() == 'GET':
            r = requests.get(url, headers=headers, auth=auth_data)

        elif http_method.upper() == 'POST':
            r = requests.post(url, data=body, headers=headers, auth=auth_data)

        elif http_method.upper() == 'PUT':
            r = requests.put(url, data=body, headers=headers, auth=auth_data)

        elif http_method.upper() == 'DELETE':
            r = requests.delete(url, data=body, headers=headers, auth=auth_data)

        elif http_method.upper() == 'OPTIONS':
            r = requests.options(url, data=body, headers=headers, auth=auth_data)

        else:
            raise Exception("Invalid request method")

        return self.handle_response(r, return_format)

    def handle_response(self, response, return_format):
        try:
            return response.json()
        except ValueError:
            return response.content