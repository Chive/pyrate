from requests_oauthlib import OAuth1

from pyrate.main import Pyrate


class TwitterPyrate(Pyrate):

    base_url = 'https://api.twitter.com/1.1/'
    http_methods = ['GET', 'POST']
    default_http_method = http_methods[0]
    return_formats = ['json']
    default_return_format = return_formats[0]
    default_body_content = {}
    default_header_content = {}
    auth_type = 'OAUTH1'
    connection_check_method = ('GET', 'account/verify_credentials')

    # These variables should be set on implementation
    oauth_consumer_key = ''
    oauth_consumer_secret = ''
    oauth_token = ''
    oauth_token_secret = ''

    def get_oauth(self):
        if self.oauth_token != "" and self.oauth_token_secret != "":
            return OAuth1(self.oauth_consumer_key,
                          client_secret=self.oauth_consumer_secret,
                          resource_owner_key=self.oauth_token,
                          resource_owner_secret=self.oauth_token_secret)
        else:
            raise Exception("Please set your oauth_token and oauth_token_secret first!")
