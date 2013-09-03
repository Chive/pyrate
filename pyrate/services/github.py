from pyrate.main import Pyrate


class GithubPyrate(Pyrate):
    # These variables must be set on instantiation
    auth_user = ''
    auth_pass = ''

    http_methods = ['GET', 'POST']
    return_formats = ['json']
    default_body_content = {}
    auth_type = 'BASIC_AUTH'
    connection_check_method = ('GET', '#')
    base_url = 'https://api.github.com/'

    def __init__(self, auth_user, auth_pass, default_http_method=None, default_return_format=None):
        super(GithubPyrate, self).__init__()
        self.auth_user = auth_user
        self.auth_pass = auth_pass
        self.default_header_content = {
            'Authorization': self.create_basic_auth(self.auth_user, self.auth_pass)
        }

        if default_http_method:
            self.default_http_method = default_http_method

        if default_return_format:
            self.default_return_format = default_return_format