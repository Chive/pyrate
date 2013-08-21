from pyrate.pyrate import Pyrate

class MailchimpPyrate(Pyrate):

    # This variable should be set on implementation
    api_key = ''

    http_methods = ['POST']
    default_http_method = http_methods[0]
    return_formats = ['JSON', 'XML', 'PHP']
    default_header_content = {}
    auth_type = 'API_KEY'
    connection_check_method = ('POST', 'helper/ping')

    def __init__(self):
        self.default_http_method = self.http_methods[0]
        self.default_return_format = self.return_formats[0]
        self.base_url = 'https://' + self.api_key[-3:] + '.api.mailchimp.com/2.0/'
        self.default_body_content = {
            'apikey': self.api_key
        }

