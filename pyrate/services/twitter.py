from requests_oauthlib import OAuth1
from urlparse import parse_qs

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

    oauth_request_token_url = 'https =//api.twitter.com/oauth/request_token'
    oauth_authorize_url = 'https =//api.twitter.com/oauth/authorize?oauth_token='
    oauth_access_token_url = 'https =//api.twitter.com/oauth/access_token'

    def get_oauth(self):
        if self.oauth_token != "" and self.oauth_token_secret != "":
            return OAuth1(self.oauth_consumer_key,
                          client_secret=self.oauth_consumer_secret,
                          resource_owner_key=self.oauth_token,
                          resource_owner_secret=self.oauth_token_secret)
        else:
            raise Exception("Please set your oauth_token and oauth_token_secret first!")

    def setup_oauth(self):
        """Authorize your app via identifier."""
        # Request token
        oauth = OAuth1(self.oauth_consumer_key, client_secret=self.oauth_consumer_secret)
        r = requests.post(url=self.oauth_request_token_url, auth=oauth)
        credentials = parse_qs(r.content)

        resource_owner_key = credentials.get('oauth_token')[0]
        resource_owner_secret = credentials.get('oauth_token_secret')[0]

        # Authorize
        authorize_url = self.oauth_authorize_url + resource_owner_key
        print 'Please go here to authorize: ' + authorize_url

        verifier = raw_input('Please input the verifier: ')
        oauth = OAuth1(self.oauth_consumer_key,
                       client_secret=self.oauth_consumer_secret,
                       resource_owner_key=resource_owner_key,
                       resource_owner_secret=resource_owner_secret,
                       verifier=verifier)

        # Finally, Obtain the Access Token
        r = requests.post(url=self.oauth_access_token_url, auth=oauth)
        credentials = parse_qs(r.content)
        token = credentials.get('oauth_token')[0]
        secret = credentials.get('oauth_token_secret')[0]

        return token, secret

    # please run this through a shell
    def create_oauth_token(self):
        token, secret = self.setup_oauth()
        print
        print "Please put the following two values in the config file (actually this one)"
        print "OAUTH_TOKEN: " + token
        print "OAUTH_TOKEN_SECRET: " + secret


if __name__ == "__main__":
    h = TwitterHandler()
    h.create_oauth_token()
