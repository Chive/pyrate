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
            return harvest.HarvestPyrate(self.credentials['harvest']['user'], self.credentials['harvest']['pass'],
                                         self.credentials['harvest']['organisation'])

        elif service == 'mailchimp':
            return mailchimp.MailchimpPyrate(self.credentials['mailchimp']['apikey'])

        elif service == 'twitter':
            return twitter.TwitterPyrate(self.credentials['twitter']['oauth_consumer_key'],
                                         self.credentials['twitter']['oauth_consumer_secret'],
                                         self.credentials['twitter']['oauth_token'],
                                         self.credentials['twitter']['oauth_token_secret'])

    def setUp(self):
        for group in self.credentials:
            for key in self.credentials[group]:
                if self.credentials[group][key] == '':
                    self.credentials[group][key] = raw_input(group + ": " + key)

    def test_twitter_con_do_geo(self):
        h = self.getHandler('twitter')

        # if this test fails, check the output of an actual request for this geo-id
        self.assertEqual(h.do('geo/id/df51dec6f4ee2b2c'), self.results['twitter']['con_do_geo'])

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
        self.assertEqual(h.do('helper/ping'), self.results['mailchimp']['con_check'])

    def test_mailchimp_con_check(self):
        h = self.getHandler('mailchimp')
        self.assertEqual(h.check_connection(), self.results['mailchimp']['con_check'])

    def test_harvest_con_do(self):
        h = self.getHandler('harvest')
        self.assertEqual(h.do('account/who_am_i'), self.results['harvest']['con_check'])

    def test_harvest_con_check(self):
        h = self.getHandler('harvest')
        self.assertEqual(h.check_connection(), self.results['harvest']['con_check'])


if __name__ == '__main__':
    unittest.main()