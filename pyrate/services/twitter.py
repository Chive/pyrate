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

    # These variables must be set on instantiation
    oauth_consumer_key = ''
    oauth_consumer_secret = ''
    oauth_token = ''
    oauth_token_secret = ''

    def __init__(self, oauth_consumer_key, oauth_consumer_secret, oauth_token, oauth_token_secret,
                 default_http_method=None, default_return_format=None):
        super(TwitterPyrate, self).__init__()
        self.oauth_consumer_key = oauth_consumer_key
        self.oauth_consumer_secret = oauth_consumer_secret
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret

        if default_http_method:
            self.default_http_method = default_http_method

        if default_return_format:
            self.default_return_format = default_return_format

    # Essential Stuff
    def get_oauth(self):
        if self.oauth_token != "" and self.oauth_token_secret != "":
            return OAuth1(self.oauth_consumer_key,
                          client_secret=self.oauth_consumer_secret,
                          resource_owner_key=self.oauth_token,
                          resource_owner_secret=self.oauth_token_secret)
        else:
            raise Exception("Please set your oauth_token and oauth_token_secret first! (Use 'pyratetools'"
                            "from command line)")

    def check_response_success(self, response):
        if not 'error' in response and not 'errors' in response:
            return True
        else:
            return self.parse_errors(response)

    def parse_errors(self, response):
        if 'error' in response:
            print("Error: %s" % response['error'])
        elif 'errors' in response:
            for error in response['errors']:
                print("Error: %s (Code: %s)" % (error['message'], error['code']))
        else:
            print("Error: %s" % response)

        return False

    # Convenience
    def tweet(self, status, in_reply_to_status_id=None, loc_lat=None, loc_long=None, place_id=None,
              display_coordinates=None,
              trim_user=None, include_entities=None):
        fargs = {'status': status, 'in_reply_to_status_id': in_reply_to_status_id, 'lat': loc_lat, 'long': loc_long,
                 'place_id': place_id, 'display_coordinates': display_coordinates, 'trim_user': trim_user,
                 'include_entities': include_entities}
        res = self.do('statuses/update', http_method='POST', content=self.build_content(fargs))
        return self.check_response_success(res)
