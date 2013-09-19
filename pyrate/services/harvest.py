from pyrate.main import Pyrate


class HarvestPyrate(Pyrate):
    # These variables must be set on instantiation
    auth_user = ''
    auth_pass = ''
    organisation_name = ''

    http_methods = ['GET', 'POST']
    return_formats = ['json']
    default_body_content = {}
    auth_type = 'BASIC_AUTH'
    connection_check_method = ('GET', 'account/who_am_i')

    def __init__(self, auth_user, auth_pass, organisation_name, default_http_method=None, default_return_format=None):
        super(HarvestPyrate, self).__init__()
        self.auth_user = auth_user
        self.auth_pass = auth_pass
        self.organisation_name = organisation_name
        self.base_url = 'https://' + self.organisation_name + '.harvestapp.com/'
        self.default_header_content = {
            'Authorization': self.create_basic_auth(self.auth_user, self.auth_pass)
        }

        if default_http_method:
            self.default_http_method = default_http_method

        if default_return_format or default_return_format == '':
            self.default_return_format = default_return_format