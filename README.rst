pyrate
======

.. image:: https://pypip.in/v/pyrate/badge.png
    :target: https://crate.io/packages/pyrate/
    :alt: Latest PyPI version

.. image:: https://pypip.in/d/pyrate/badge.png
    :target: https://crate.io/packages/pyrate/
    :alt: Number of PyPI downloads
    

Pyrate is a python wrapper for restful web apis. It's like *magic* but
simpler.

Currently, the following services are implemented

-  `Github <#github>`__
-  `Harvest <#harvest>`__
-  `Basecamp <#basecamp>`__
-  `Mailchimp (v2) <#mailchimp>`__
-  `Twitter (v1.1 + OAuth) <#twitter>`__

There's a quick-start guide below, for full documentation (WIP) visit: `http://pyrate.readthedocs.org/en/latest/ <http://pyrate.readthedocs.org/en/latest/>`__

Dependencies
------------

-  `requests <http://python-requests.org>`__
-  `requests\_oauthlib <https://github.com/requests/requests-oauthlib>`__

Install
-------

::

    # so simple
    pip install pyrate

Quick Start
-----------

Twitter
~~~~~~~

::

    from pyrate.services import twitter

    h = twitter.TwitterPyrate('oauth_consumer_key', 'oauth_consumer_secret',
                              'oauth_token', 'oauth_token_secret')

    print(h.do('account/verify_credentials'))
    print(h.check_connection())
    h.tweet("This is awesome!")

Mailchimp
~~~~~~~~~

::

    from pyrate.services import mailchimp

    h = mailchimp.MailchimpPyrate('apikey')

    print(h.do('helper/ping'))
    print(h.check_connection())
    h.subscribeToList('ListName', 'myemail@example.com')
    h.unsubscribeFromList('ListName', 'myemail@example.com')

Harvest
~~~~~~~

::

    from pyrate.services import harvest

    h = harvest.HarvestPyrate('user', 'password', 'organisation')

    print(h.do('account/who_am_i'))
    print(h.check_connection())

Github
~~~~~~

::

    from pyrate.services import github

    h = github.GithubPyrate('user', 'password')

    print(h.do('#'))
    print(h.check_connection())
    h.create_repo('name', 'description', private=True)
    h.create_repo('name', 'description', 'organisation')
    h.delete_repo('name')

Basecamp
~~~~~~

::

    from pyrate.services import basecamp

    h = basecamp.BasecampPyrate('user', 'password', 'org_id')

    print(h.do('projects'))
    h.check_connection()

Todos
-----

-  Create more "convenience"-methods (like
   ``h.tweet("This is awesome!")``)
-  Implement CLI-Interface (see branch
   `feature/cli <https://github.com/Chive/pyrate/tree/feature/cli>`__)
-  Add more services (Open for suggestions!)
-  Expand Documentation
-  lots and lots more

