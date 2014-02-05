import unittest
import sys
from httmock import urlmatch, HTTMock, response

sys.path.append('../pyrate')  # we want the local version and not the installed one
from pyrate.services import basecamp, github, harvest, mailchimp, twitter


# In order to use these tests you need to:
# - copy credentials.py.template -> credentials.py and fill in your credentials
# - copy results.py.template -> results.py and fill in results (get them with a rest-client or requests)

class TestSequenceFunctions(unittest.TestCase):

    def getHandler(self, service):
        if service == 'github':
            return github.GithubPyrate("email@example.com", "mypass")

        elif service == 'harvest':
            return harvest.HarvestPyrate("email@example.com", "mypass", "myorganisation")

        elif service == 'mailchimp':
            return mailchimp.MailchimpPyrate("myapikey-us2")

        elif service == 'twitter':
            return twitter.TwitterPyrate("000", "000", "000", "000")

        elif service == 'basecamp':
            return basecamp.BasecampPyrate("email@example.com", "mypass", "123456")


    # TODO: Improve urlmatch regex's

    ##############################################
    ## TWITTER
    ##############################################

    @urlmatch(netloc=r'api\.twitter\.com')
    def mock_twitter(self, url, request):
        headers = {
            'status_code': 200,
        }
        content = {'id': '1', 'geometry': '0000'}
        return response(200, content, headers)

    def test_twitter_con_do_geo(self):
        h = self.getHandler('twitter')
        with HTTMock(self.mock_twitter):
            self.assertTrue('geometry' in h.get('geo/id/df51dec6f4ee2b2c'))

    def test_twitter_tweet(self):
        h = self.getHandler('twitter')
        with HTTMock(self.mock_twitter):
            self.assertTrue(h.tweet("test"))

    ##############################################
    ## MAILCHIMP
    ##############################################

    @urlmatch(netloc=r'.*\.api\.mailchimp\.com')
    def mock_mailchimp(self, url, request):
        headers = {
            'status_code': 200,
        }
        content = {'msg': "Everything's Chimpy!"}
        return response(200, content, headers)

    def test_mailchimp_con_do(self):
        h = self.getHandler('mailchimp')
        with HTTMock(self.mock_mailchimp):
            self.assertEqual(h.get('helper/ping'), {'msg': "Everything's Chimpy!"})

    def test_mailchimp_con_check(self):
        h = self.getHandler('mailchimp')
        with HTTMock(self.mock_mailchimp):
            self.assertTrue(h.check_connection())

    ##############################################
    ## HARVEST
    ##############################################

    @urlmatch(netloc=r'.*\.harvestapp\.com')
    def mock_harvest(self, url, request):
        headers = {
            'status_code': 200,
            'content-type': 'application/json',
        }
        content = {'user': 'someone', 'company': 'somecompany'}
        return response(200, content, headers)

    def test_harvest_con_do(self):
        h = self.getHandler('harvest')
        with HTTMock(self.mock_harvest):
            res = h.get('account/who_am_i')
        self.assertTrue('company' in res and 'user' in res)

    def test_harvest_con_check(self):
        h = self.getHandler('harvest')
        with HTTMock(self.mock_harvest):
            self.assertTrue(h.check_connection())

    ##############################################
    ## GITHUB
    ##############################################

    @urlmatch(netloc=r'api\.github\.com')
    def mock_github(self, url, request):
        headers = {
            'status_code': 200,
            'content-type': 'application/json',
        }
        content = {'current_user_url': 'github.com/someuser'}
        return response(200, content, headers)

    def test_github_con_do(self):
        h = self.getHandler('github')
        with HTTMock(self.mock_github):
            self.assertTrue('current_user_url' in h.get('#'))

    def test_github_con_check(self):
        h = self.getHandler('github')
        with HTTMock(self.mock_github):
            self.assertTrue(h.check_connection())


    ##############################################
    ## BASECAMP
    ##############################################

    @urlmatch(netloc=r'basecamp\.com')
    def mock_basecamp(self, url, request):
        headers = {
            'status_code': 200,
            'content-type': 'application/json',
        }
        content = {'email_address': "email@example.com"}
        return response(200, content, headers)

    def test_basecamp_con_check(self):
        h = self.getHandler('basecamp')
        with HTTMock(self.mock_basecamp):
            self.assertTrue(h.check_connection())



    # FIXME: Test Suites not working
    '''
    test_basecamp = unittest.TestSuite()
    test_basecamp.addTests(test_basecamp_con_check)

    test_github = unittest.TestSuite()
    test_github.addTests(test_github_con_check)
    test_github.addTests(test_github_con_do)

    test_harvest = unittest.TestSuite()
    test_harvest.addTests(test_harvest_con_check)
    test_harvest.addTests(test_harvest_con_do)

    test_mailchimp = unittest.TestSuite()
    test_mailchimp.addTests(test_mailchimp_con_check)
    test_mailchimp.addTests(test_mailchimp_con_do)

    test_twitter = unittest.TestSuite()
    test_twitter.addTests(test_twitter_con_do_geo)
    test_twitter.addTests(test_twitter_tweet)

    alltests = unittest.TestSuite([test_basecamp, test_github, test_harvest, test_mailchimp, test_twitter])
    '''

if __name__ == '__main__':
    #unittest.TextTestRunner().run(test_basecamp)
    unittest.main()
