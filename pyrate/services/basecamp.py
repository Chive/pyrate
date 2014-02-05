from pyrate.main import Pyrate


class BasecampPyrate(Pyrate):

    # request
    base_url = None
    default_header_content = None
    default_body_content = None
    auth_data = {'type': 'BASIC'}
    send_json = True

    # response
    response_formats = ['json']
    default_response_format = None
    validate_response = True

    connection_check = {'http_method': 'GET', 'target': 'people/me'}

    def __init__(self, auth_user, auth_pass, org_id, default_response_format=None):
        super(BasecampPyrate, self).__init__()
        self.auth_data['username'] = auth_user
        self.auth_data['password'] = auth_pass
        self.auth_data['org_id'] = org_id
        self.base_url = 'https://basecamp.com/' + org_id + '/api/v1/'
        self.default_header_content = {
            'Authorization': self.get_auth_data(),
            'User Agent': 'Pyrate'
        }

        if default_response_format:
            self.default_response_format = default_response_format
        else:
            self.default_response_format = self.response_formats[0]
