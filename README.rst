pyrate
======

Pyrate is a python wrapper for restful web apis. It's like *magic* but
simpler.

Currently, the following services are implemented

-  Twitter (v1.1 + OAuth)
-  Mailchimp (v2)
-  Harvest

Dependencies
------------

-  `requests <http://python-requests.org>`__
-  `requests\_oauthlib <https://github.com/requests/requests-oauthlib>`__

Install
-------

::

    # so simple
    pip install pyrate

Usage
-----

Twitter
~~~~~~~

::

    from pyrate.services import twitter

    h = twitter.TwitterPyrate('oauth_consumer_key', 'oauth_consumer_secret',
                              'oauth_token', 'oauth_token_secret')

    print(h.do('account/verify_credentials'))
    print(h.check_connection())
    print(h.tweet("This is awesome!"))

Mailchimp
~~~~~~~~~

::

    from pyrate.services import mailchimp

    h = mailchimp.MailchimpPyrate('apikey')

    print(h.do('helper/ping'))
    print(h.check_connection())
    print(h.subscribeToList('ListName', 'myemail@example.com'))
    print(h.unsubscribeFromList('ListName', 'myemail@example.com'))

Harvest
~~~~~~~

::

    from pyrate.services import harvest

    h = harvest.HarvestPyrate('user', 'password', 'organisation')

    print(h.do('account/who_am_i'))
    print(h.check_connection())

Todos
-----

-  Create more "convenience"-methods (like
   ``h.tweet("This is awesome!")``)
-  Implement CLI-Interface (see branch
   `cli-interface <https://github.com/Chive/pyrate/tree/cli-interface>`__
-  Add more services (Open for suggestions!)
-  Create Documentation
-  lots and lots more

