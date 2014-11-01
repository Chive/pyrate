# pyrate

[![Latest PyPI version](https://pypip.in/v/pyrate/badge.png)](https://crate.io/packages/pyrate/) [![Number of PyPI downloads](https://pypip.in/d/pyrate/badge.png)](https://crate.io/packages/pyrate/) [![Build Status](https://travis-ci.org/Chive/pyrate.png?branch=master)](https://travis-ci.org/Chive/pyrate) [![Code Coverage](https://coveralls.io/repos/Chive/pyrate/badge.png?branch=master)](https://coveralls.io/r/Chive/pyrate?branch=master)

Pyrate is a python wrapper for restful web apis. It's like *magic* but
simpler.

> **Note:** Active development is happening here: [``feature/0.5.0``](https://github.com/Chive/pyrate/tree/feature/0.5.0)

Currently, the following services are implemented


*  [GitHub](#github)
*  [Harvest](#harvest)
*  [Basecamp](#basecamp)
*  [Mailchimp (v2)](#mailchimp)
*  [Twitter (v1.1 + OAuth)](#twitter)

There's a quick-start guide below, for full documentation (WIP) visit: [readthedocs.org/en/latest](http://pyrate.readthedocs.org/en/latest/)

## Dependencies

*  [``requests``](http://python-requests.org)
*  [``requests_oauthlib``](https://github.com/requests/requests-oauthlib)

## Installation

```bash
$ pip install pyrate
```

## Quick Start

### <a name="twitter">Twitter</a>

```python
from pyrate.services import twitter

h = twitter.TwitterPyrate(
    'oauth_consumer_key', 'oauth_consumer_secret',
    'oauth_token', 'oauth_token_secret'
)

# check if the connection works
h.check_connection()

# direct api call
h.do('account/verify_credentials')

# convenient tweeting!
h.tweet("This is awesome!")
```

### <a name="mailchimp">Mailchimp</a>

```python
from pyrate.services import mailchimp

h = mailchimp.MailchimpPyrate('apikey')

# check if the connection works
h.check_connection()

# direct api call
h.do('helper/ping')

# (un)subscribing to lists!
h.subscribeToList('ListName', 'myemail@example.com')
h.unsubscribeFromList('ListName', 'myemail@example.com')
```

### <a name="harvest">Harvest</a>

```python
from pyrate.services import harvest

h = harvest.HarvestPyrate('user', 'password', 'organisation')

# check if the connection works
h.check_connection()

# tell me who I am    
h.do('account/who_am_i')
```

### <a name="github">GitHub</a>

```python
from pyrate.services import github

h = github.GithubPyrate('user', 'password')

# check if the connection works
h.check_connection()

# create & delete repositories
h.create_repo('name', 'description', private=True)
h.create_repo('name', 'description', 'organisation')
h.delete_repo('name')
```

### <a name="basecamp">Basecamp</a>

```python
from pyrate.services import basecamp

h = basecamp.BasecampPyrate('user', 'password', 'org_id')

# check if the connection works
h.check_connection()

# show existing projects
print(h.do('projects'))
```

Todos
-----

*  Create more "convenience"-methods (like ``h.tweet()``)
*  Implement CLI-Interface (see branch [``feature/cli``](https://github.com/Chive/pyrate/tree/feature/cli>))
*  Add more services (open for suggestions!)
*  Expand documentation
*  lots and lots more
