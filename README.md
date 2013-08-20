pyrate
======
Pyrate is a python wrapper for restful web apis. It's like *magic* but quicker.

Currently, the following services are implemented

* Twitter (v1.1 + OAuth)
* Mailchimp (v2)
* Harvest

Dependencies
------------
* [requests](http://python-requests.org)
* [requests_oauthlib](https://github.com/requests/requests-oauthlib)

Usage
-----
### Twitter
```
from services import twitter

class myTwitterPyrate(twitter.TwitterPyrate):
    oauth_consumer_key = ''
    oauth_consumer_secret = ''

    oauth_token = ''
    oauth_token_secret = ''

h = myTwitterPyrate()
print h.do('account/verify_credentials')
print h.check_connection()
```
### Mailchimp
```
from services import mailchimp

class myMailchimpPyrate(mailchimp.MailchimpPyrate):
    api_key = ''

h = myMailchimpPyrate()
print h.do('helper/ping')
print h.check_connection()
```
### Harvest
```
from services import harvest

class myHarvestPyrate(harvest.HarvestPyrate):
    auth_user = ''
    auth_pass = ''
    organisation_name = ''

h = myHarvestPyrate()
print h.do('account/who_am_i')
print h.check_connection()
```