import json
import requests


class Pyrate:

    http_methods = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
    return_formats = ['json']
    default_header_content = None
    default_body_content = None
    default_http_method = None
    default_return_format = None
    connection_check_method = None
    auth_type = None
    api_key = None
    base_url = None

    def __init__(self):
        self.default_http_method = self.http_methods[0]
        self.default_return_format = self.return_formats[0]

    def get_oauth(self):
        raise NotImplementedError("OAuth methods need to be implemented by subclasses!")

    def check_connection(self):
        return self.do(self.connection_check_method[1], http_method=self.connection_check_method[0])

    # takes a dictionary, filters out all the empty stuff
    def build_content(self, args):
        del args['self']
        new_args = args.copy()

        for key in args:
            if not args[key]:
                del new_args[key]

        return new_args

    def check_response_success(self, response, key, value):
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
        request_headers = self.default_header_content
        request_body = self.default_body_content

        return self.do_request(http_method, request_url, request_headers, request_body, return_format)

    def do_request(self, http_method, url, headers, body, return_format):

        if self.auth_type == 'OAUTH1':
            auth_data = self.get_oauth()
        else:
            auth_data = None

        if http_method.upper() == 'GET':
            r = requests.get(url, headers=headers, auth=auth_data)

        elif http_method.upper() == 'POST':
            r = requests.post(url, params=body, headers=headers, auth=auth_data)

        elif http_method.upper() == 'PUT':
            r = requests.put(url, params=body, headers=headers, auth=auth_data)

        elif http_method.upper() == 'DELETE':
            r = requests.delete(url, params=body, headers=headers, auth=auth_data)

        elif http_method.upper() == 'OPTIONS':
            r = requests.options(url, params=body, headers=headers, auth=auth_data)

        return self.handle_response(r, return_format)

    def handle_response(self, response, return_format):
        try:
            return response.json()
        except ValueError:
            return response.content