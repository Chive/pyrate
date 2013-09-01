from base64 import b64encode
import sys
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

        # Messing around with Python3's strictness about strings
        if sys.version_info >= (3, 0):
            if isinstance(auth_user, str):
                auth_user = self.auth_user
            else:
                auth_user = self.auth_user.decode('utf-8')

            if isinstance(auth_pass, str):
                auth_pass = self.auth_pass
            else:
                auth_pass = self.auth_pass.decode('utf-8')

            auth = b64encode((auth_user + ":" + auth_pass).encode('utf-8')).decode('utf-8')

        else:
            auth = b64encode(self.auth_user + ":" + self.auth_pass).rstrip()

        self.default_header_content = {
            'Authorization': 'Basic ' + auth
        }

        if default_http_method:
            self.default_http_method = default_http_method

        if default_return_format:
            self.default_return_format = default_return_format