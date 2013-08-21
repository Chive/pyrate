import base64
from pyrate.main import Pyrate


class HarvestPyrate(Pyrate):

    # These variables should be set on implementation
    auth_user = ''
    auth_pass = ''
    organisation_name = ''

    http_methods = ['GET', 'POST']
    return_formats = ['json']
    default_body_content = {}
    auth_type = 'BASIC_AUTH'
    connection_check_method = ('GET', 'account/who_am_i')

    def __init__(self):
        self.base_url = 'https://' + self.organisation_name + '.harvestapp.com/'
        self.default_http_method = self.http_methods[0]
        self.default_return_format = self.return_formats[0]
        self.default_header_content = {
            'Authorization': 'Basic ' + base64.b64encode(self.auth_user + ":" + self.auth_pass).rstrip()
        }