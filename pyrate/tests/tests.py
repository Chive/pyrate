from random import choice
import unittest
import sys
import os

sys.path.append('../pyrate')  # we want the local version and not the installed one
from pyrate.services import github, harvest, mailchimp, twitter


# In order to use these tests you need to:
# - copy credentials.py.template -> credentials.py and fill in your credentials
# - copy results.py.template -> results.py and fill in results (get them with a rest-client or requests)

class TestSequenceFunctions(unittest.TestCase):

    try:
        travis = os.environ['TRAVIS']
    except KeyError:
        travis = False

    if travis:
        f = open('pyrate/tests/travis_credentials')
        cipher = f.read()
        from Crypto.Cipher import AES
        import pickle
        decrypter = AES.new(os.environ['crypt_key'], AES.MODE_CBC, os.environ['crypt_iv'])
        credentials = pickle.loads(decrypter.decrypt(cipher))

    else:
        try:
            import credentials
        except ImportError:
            raise ImportError("Module credentials could not be found. You probably have to modify the template first.")
        credentials = credentials.credentials

    def getHandler(self, service):
        if service == 'github':
            return github.GithubPyrate(self.credentials['github']['user'], self.credentials['github']['pass'])
        elif service == 'harvest':
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
        self.assertTrue('geometry' in h.do('geo/id/df51dec6f4ee2b2c'))

    def test_twitter_tweet(self):
        h = self.getHandler('twitter')

        # to prevent duplicate statuses we use a random string
        rand = ''.join(choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(16))
        text = "Testing #pyrate https://chive.github.io/pyrate [" + rand + "]"
        res = h.tweet(text)
        
        self.assertTrue(res)

    def test_mailchimp_con_do(self):
        h = self.getHandler('mailchimp')
        self.assertEqual(h.do('helper/ping'), {u'msg': u"Everything's Chimpy!"})

    def test_mailchimp_con_check(self):
        h = self.getHandler('mailchimp')
        self.assertEqual(h.check_connection(), {u'msg': u"Everything's Chimpy!"})

    def test_harvest_con_do(self):
        h = self.getHandler('harvest')
        res = h.do('account/who_am_i')
        self.assertTrue('company' in res and 'user' in res)

    def test_harvest_con_check(self):
        h = self.getHandler('harvest')
        res = h.check_connection()
        self.assertTrue('company' in res and 'user' in res)

    def test_github_con_do(self):
        h = self.getHandler('github')
        res = h.do('#')
        self.assertTrue('current_user_url' in res)

    def test_github_con_check(self):
        h = self.getHandler('github')
        res = h.check_connection()
        self.assertTrue('current_user_url' in res)


if __name__ == '__main__':
    unittest.main()
