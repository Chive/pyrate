pyrate
======

.. image:: https://pypip.in/d/pyrate/badge.png
    :target: https://crate.io/packages/pyrate/
    :alt: Number of PyPI downloads
    
.. image:: https://travis-ci.org/Chive/pyrate.png?branch=master
    :target: https://travis-ci.org/Chive/pyrate
    :alt: Build Status

.. image:: https://coveralls.io/repos/Chive/pyrate/badge.png?branch=master
    :target: https://coveralls.io/r/Chive/pyrate?branch=master
    :alt: Code Coverage

.. image:: https://d2weczhvl823v0.cloudfront.net/Chive/pyrate/trend.png
    :alt: Bitdeli Badge

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

Installation
------------

::

    pip install pyrate

Quick Start
-----------

Twitter
~~~~~~~

::

    from pyrate.services import twitter

    h = twitter.TwitterPyrate(
        oauth_consumer_key='',
        oauth_consumer_secret='',
        oauth_token='',
        oauth_token_secret=''
    )

    # check if the connection works
    h.check_connection()
    
    # direct api call
    h.get('account/verify_credentials')
    
    # convenient tweeting!
    h.tweet("This is awesome!")

Mailchimp
~~~~~~~~~

::

    from pyrate.services import mailchimp

    h = mailchimp.MailchimpPyrate(apikey='')

    # check if the connection works
    h.check_connection()
    
    # direct api call
    h.do('helper/ping')
    
    # (un)subscribing to lists!
    h.subscribeToList('ListName', 'myemail@example.com')
    h.unsubscribeFromList('ListName', 'myemail@example.com')

Harvest
~~~~~~~

::

    from pyrate.services import harvest

    h = harvest.HarvestPyrate(
        user='',
        password='',
        organisation=''
    )

    # check if the connection works
    h.check_connection()

    # tell me who I am    
    h.do('account/who_am_i')

Github
~~~~~~

::

    from pyrate.services import github

    h = github.GithubPyrate(
        user='',
        password=''
    )
    
    # check if the connection works
    h.check_connection()
    
    # create & delete repositories!
    h.create_repo('name', 'description', private=True)
    h.create_repo('name', 'description', 'organisation')
    h.delete_repo('name')

Basecamp
~~~~~~

::

    from pyrate.services import basecamp

    h = basecamp.BasecampPyrate(
        user='',
        password='',
        org_id=''
    )

    # check if the connection works
    h.check_connection()
    
    # what projects are there?
    print(h.do('projects'))

Todos
-----

-  Create more "convenience"-methods (like
   ``h.tweet()``)
-  Implement CLI-Interface (see branch
   `feature/cli <https://github.com/Chive/pyrate/tree/feature/cli>`__)
-  Add more services (Open for suggestions!)
-  Expand Documentation
-  lots and lots more

