#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import requests
from requests_oauthlib import OAuth1
from urlparse import parse_qs


def twitter_oauth():
    print()
    print()
    print()
    os.system("clear")
    print("Twitter OAuth")
    print("-------------")
    print()
    oauth_consumer_key = raw_input("Please enter your OAuth Consumer Key: ")
    oauth_consumer_secret = raw_input("Please enter your OAuth Consumer Secret: ")

    oauth_token, oauth_token_secret = setup_twitter_oauth(oauth_consumer_key, oauth_consumer_secret)

    print("These are your OAuth tokens. You need them for the TwitterPyrate.")
    print("OAuth Token: " + oauth_token)
    print("OAuth Token Secret: " + oauth_token_secret)

def setup_twitter_oauth(oauth_consumer_key, oauth_consumer_secret):

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
    print('Please go here to authorize:')
    print(authorize_url)

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

# When were adding more we'll use docopt!
def main():
    os.system("clear")
    print("                         _")
    print("                        | |")
    print("   _ __  _   _ _ __ __ _| |_ ___")
    print("  | '_ \| | | | '__/ _` | __/ _ \ ")
    print("  | |_) | |_| | | | (_| | ||  __/")
    print("  | .__/ \__, |_|  \__,_|\__\___|")
    print("  | |     __/ |")
    print("  |_|    |___/")
    print()
    print()

    print("# These is Pyrate's commandline tool. For the usage of pyrate,")
    print("# please read the docs: https://github.com/Chive/pyrate")
    print("")
    print()
    print("# Tasks")
    print("1 Generate Twitter OAuth Tokens")
    print("0 Exit")
    print()
    c = raw_input("Your Choice: ")

    if c == '1':
        twitter_oauth()

    elif c == '0':
        exit("Goodbye")

    else:
        exit("Invalid choice. Goodbye")
