from pyrate.main import Pyrate


class HarvestPyrate(Pyrate):

    # request
    base_url = None  # see __init__
    default_header_content = None
    default_body_content = None
    auth_data = {'type': 'BASIC'}
    send_json = False

    # response
    response_formats = ['json']
    default_response_format = None
    validate_response = True

    connection_check = {'http_method': 'GET', 'target': 'account/who_am_i'}

    def __init__(self, auth_user, auth_pass, organisation_name, default_response_format=None):
        super(HarvestPyrate, self).__init__()
        self.auth_data['username'] = auth_user
        self.auth_data['password'] = auth_pass
        self.auth_data['organisation_name'] = organisation_name
        self.base_url = 'https://' + organisation_name + '.harvestapp.com/'
        self.default_header_content = {
            'Authorization': self.get_auth_data()
        }

        if default_response_format or default_response_format == '':
            self.default_response_format = default_response_format
