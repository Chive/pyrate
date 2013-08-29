from random import randrange
import unittest

from pyrate.services import twitter, harvest, mailchimp
import credentials
import results


# In order to use these tests you need to:
# - copy credentials.py.template -> credentials.py and fill in your credentials
# - copy results.py.template -> results.py and fill in results (get them with a rest-client or requests)

class TestSequenceFunctions(unittest.TestCase):

    credentials = credentials.credentials
    results = results.results

    def getHandler(self, service):
        if service == 'harvest':
            class myHarvestPyrate(harvest.HarvestPyrate):
                auth_user = self.credentials['harvest']['user']
                auth_pass = self.credentials['harvest']['pass']
                organisation_name = self.credentials['harvest']['organisation']

            return myHarvestPyrate()

        elif service == 'mailchimp':
            class myMailchimpPyrate(mailchimp.MailchimpPyrate):
                api_key = self.credentials['mailchimp']['apikey']

            return myMailchimpPyrate()

        elif service == 'twitter':
            class myTwitterPyrate(twitter.TwitterPyrate):
                oauth_consumer_key = self.credentials['twitter']['oauth_consumer_key']
                oauth_consumer_secret = self.credentials['twitter']['oauth_consumer_secret']
                oauth_token = self.credentials['twitter']['oauth_token']
                oauth_token_secret = self.credentials['twitter']['oauth_token_secret']

            return myTwitterPyrate()

    def setUp(self):
        for group in self.credentials:
            for key in self.credentials[group]:
                if self.credentials[group][key] == '':
                    self.credentials[group][key] = raw_input(group + ": " + key)

    def test_twitter_con_do_geo(self):
        h = self.getHandler('twitter')

        # if this test fails, check the output of an actual request for this geo-id
        self.assertEqual(h.do('geo/id/df51dec6f4ee2b2c'), results['twitter']['con_do_geo'])

    def test_twitter_tweet(self):
        h = self.getHandler('twitter')

        # to prevent duplicate statuses we use a random amount of o's in "so"
        text = "Pyrate is s"
        i = 0
        while i < randrange(5):
            text += "o"
        text += " great! #pyrate https://github.com/Chive/pyrate"

        self.assertEqual(h.tweet(text), True)

    def test_mailchimp_con_do(self):
        h = self.getHandler('mailchimp')
        self.assertEqual(h.do('helper/ping'), results['mailchimp']['con_check'])

    def test_mailchimp_con_check(self):
        h = self.getHandler('mailchimp')
        self.assertEqual(h.check_connection(), results['mailchimp']['con_check'])

    def test_harvest_con_do(self):
        h = self.getHandler('harvest')
        self.assertEqual(h.do('account/who_am_i'), results['harvest']['con_check'])

    def test_harvest_con_check(self):
        h = self.getHandler('harvest')
        self.assertEqual(h.check_connection(), results['harvest']['con_check'])


if __name__ == '__main__':
    unittest.main()