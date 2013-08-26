pyrate
======
Pyrate is a python wrapper for restful web apis. It's like *magic* but simpler.

Currently, the following services are implemented

* Twitter (v1.1 + OAuth)
* Mailchimp (v2)
* Harvest

Dependencies
------------
* [requests](http://python-requests.org)
* [requests_oauthlib](https://github.com/requests/requests-oauthlib)

Install
-------
```
# so simple
pip install pyrate
```

Usage
-----
### Twitter
```
from pyrate.services import twitter

class MyTwitterPyrate(twitter.TwitterPyrate):
    oauth_consumer_key = ''
    oauth_consumer_secret = ''

    oauth_token = ''
    oauth_token_secret = ''

h = MyTwitterPyrate()

print h.do('account/verify_credentials')

print h.check_connection()

print h.tweet("This is awesome!")
```
### Mailchimp
```
from pyrate.services import mailchimp

class MyMailchimpPyrate(mailchimp.MailchimpPyrate):
    api_key = ''

h = MyMailchimpPyrate()

print h.do('helper/ping')

print h.check_connection()
```
### Harvest
```
from pyrate.services import harvest

class MyHarvestPyrate(harvest.HarvestPyrate):
    auth_user = ''
    auth_pass = ''
    organisation_name = ''

h = MyHarvestPyrate()

print h.do('account/who_am_i')

print h.check_connection()
```
Todos
-----
* Create more "convenience"-methods (like ```h.tweet("This is awesome!")```)
* Implement CLI-Interface (see branch [cli-interface](https://github.com/Chive/pyrate/tree/cli-interface)
* Add more services (Open for suggestions!)
* lots and lots more
