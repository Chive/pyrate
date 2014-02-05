from pyrate.main import Pyrate
from pyrate.utils import clean_dict


class TwitterPyrate(Pyrate):

    # request
    base_url = 'https://api.twitter.com/1.1/'
    default_header_content = None
    default_body_content = None
    auth_data = {
        'type': 'OAUTH1',
        'client_key': None, 'client_secret': None,
        'token_key': None, 'token_secret': None
    }
    send_json = False

    # response
    response_formats = ['json']
    default_response_format = response_formats[0]
    validate_response = True

    connection_check = {
        'http_method': 'GET',
        'target': 'account/verify_credentials'
    }

    def __init__(self, oauth_consumer_key, oauth_consumer_secret, oauth_token,
                 oauth_token_secret, default_response_format=None):
        super(TwitterPyrate, self).__init__()
        self.auth_data['client_key'] = oauth_consumer_key
        self.auth_data['client_secret'] = oauth_consumer_secret
        self.auth_data['token_key'] = oauth_token
        self.auth_data['token_secret'] = oauth_token_secret

        if default_response_format:
            self.default_response_format = default_response_format

    # Convenience
    def tweet(self, status, in_reply_to_status_id=None, loc_lat=None,
              loc_long=None, place_id=None, display_coordinates=None,
              trim_user=None, include_entities=None):

        return self.post('statuses/update', content=clean_dict({
            'status': status, 'in_reply_to_status_id': in_reply_to_status_id,
            'lat': loc_lat, 'long': loc_long, 'place_id': place_id,
            'display_coordinates': display_coordinates, 'trim_user': trim_user,
            'include_entities': include_entities
        }))
