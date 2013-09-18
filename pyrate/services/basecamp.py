from pyrate.main import Pyrate


class BasecampPyrate(Pyrate):
    # These variables must be set on instantiation
    auth_user = ''
    auth_pass = ''
    org_id = ''

    http_methods = ['GET', 'POST', 'PATCH', 'DELETE']
    return_formats = ['json']
    default_body_content = {}
    auth_type = 'BASIC_AUTH'
    connection_check_method = ('GET', 'people/me')
    send_json = True

    def __init__(self, auth_user, auth_pass, org_id, default_http_method=None, default_return_format=None):
        super(BasecampPyrate, self).__init__()
        self.auth_user = auth_user
        self.auth_pass = auth_pass
        self.org_id = org_id
        self.base_url = 'https://basecamp.com/' + self.org_id + '/api/v1/'

        self.default_header_content = {
            'Authorization': self.create_basic_auth(self.auth_user, self.auth_pass),
            'User Agent': 'Pyrate (' + auth_user + ')'
        }

        if default_http_method:
            self.default_http_method = default_http_method

        if default_return_format:
            self.default_return_format = default_return_format
        else:
            self.default_return_format = self.return_formats[0]

    def check_connection(self):
        res = self.do(self.connection_check_method[1], http_method=self.connection_check_method[0])
        if 'email_address' in res and res['email_address'] == self.auth_user:
            return True
        else:
            return res
