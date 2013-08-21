import requests
from requests_oauthlib import OAuth1
from urlparse import parse_qs


def setup_oauth(oauth_consumer_key, oauth_consumer_secret):

    oauth_request_token_url = 'https://api.twitter.com/oauth/request_token'
    oauth_authorize_url = 'https://api.twitter.com/oauth/authorize?oauth_token='
    oauth_access_token_url = 'https://api.twitter.com/oauth/access_token'

    """Authorize your app via identifier."""
    # Request token
    oauth = OAuth1(oauth_consumer_key, client_secret=oauth_consumer_secret)
    r = requests.post(url=oauth_request_token_url, auth=oauth)
    credentials = parse_qs(r.content)

    resource_owner_key = credentials.get('oauth_token')[0]
    resource_owner_secret = credentials.get('oauth_token_secret')[0]

    # Authorize
    authorize_url = oauth_authorize_url + resource_owner_key
    print 'Please go here to authorize:'
    print authorize_url

    verifier = raw_input('Please input the verifier: ')
    oauth = OAuth1(oauth_consumer_key,
                   client_secret=oauth_consumer_secret,
                   resource_owner_key=resource_owner_key,
                   resource_owner_secret=resource_owner_secret,
                   verifier=verifier)

    # Finally, Obtain the Access Token
    r = requests.post(url=oauth_access_token_url, auth=oauth)
    credentials = parse_qs(r.content)
    token = credentials.get('oauth_token')[0]
    secret = credentials.get('oauth_token_secret')[0]

    return token, secret


if __name__ == "__main__":
    print "Twitter OAuth"
    print "#############"
    print
    oauth_consumer_key = raw_input("Please enter your OAuth Consumer Key: ")
    oauth_consumer_secret = raw_input("Please enter your OAuth Consumer Secret: ")

    oauth_token, oauth_token_secret = setup_oauth(oauth_consumer_key, oauth_consumer_secret)

    print "These are your OAuth tokens. You need them for the TwitterPyrate."
    print "OAuth Token: " + oauth_token
    print "OAuth Token Secret: " + oauth_token_secret