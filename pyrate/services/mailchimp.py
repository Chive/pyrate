from pyrate.main import Pyrate


class ListNotFoundError(Exception):
    pass


class MailchimpPyrate(Pyrate):
    # This variable must be set on instantiation
    api_key = ''

    http_methods = ['POST']
    default_http_method = http_methods[0]
    return_formats = ['JSON', 'XML', 'PHP']
    default_header_content = {}
    auth_type = 'API_KEY'
    connection_check_method = ('POST', 'helper/ping')
    send_json = True

    def __init__(self, apikey, default_http_method=None, default_return_format=None):
        super(MailchimpPyrate, self).__init__()
        self.api_key = apikey
        self.base_url = 'https://' + self.api_key[-3:] + '.api.mailchimp.com/2.0/'
        self.default_body_content = {
            'apikey': self.api_key
        }

        if default_http_method:
            self.default_http_method = default_http_method

        if default_return_format:
            self.default_return_format = default_return_format

    def check_response_success(self, response):
        if 'error' not in response:
            if 'errors' in response:
                if response['errors'] == []:
                    return True
                else:
                    return False
            return True
        else:
            self.parse_errors(response)
            return False

    def parse_errors(self, response):
        if 'error' in response:
            print("Error: %s (Code: %s)" % (response['error'], response['code']))
        elif 'errors' in response:
            for error in response['errors']:
                print("Error: %s (Code: %s)" % (error['error'], error['code']))
                print(error['param'])
        else:
            print("Error: %s" % response)

    # http://apidocs.mailchimp.com/api/2.0/lists/list.php
    def getLists(self, filters=None, start=None, limit=None, sort_field=None, sort_dir=None):
        fargs = locals()
        res = self.do('lists/list', http_method='POST', content=self.build_content(fargs))
        if self.check_response_success(res):
            return res['data']
        else:
            return res

    def getListByName(self, list_name):
        lists = self.getLists()
        for l in lists:
            if l['name'] == list_name:
                return l

        # else
        raise ListNotFoundError()

    # http://apidocs.mailchimp.com/api/2.0/lists/subscribe.php
    def subscribeToList(self, list_name, user_email, merge_vars=None, email_type=None, double_optin=None, update_existing=None,
                        replace_interests=None, send_welcome=None):

        list_id = self.getListByName(list_name)['id']
        fargs = {'id': list_id, 'email': {'email': user_email}, 'merge_vars': merge_vars, 'email_type': email_type,
                 'double_optin': double_optin, 'update_existing': update_existing,
                 'replace_interests': replace_interests, 'send_welcome': send_welcome}

        return self.do('lists/subscribe', http_method='POST', content=self.build_content(fargs))
        # return self.check_response_success(res)

    # http://apidocs.mailchimp.com/api/2.0/lists/unsubscribe.php
    def unsubscribeFromList(self, list_name, user_email, delete_member=None, send_goodbye=None, send_notify=None):
        list_id = self.getListByName(list_name)['id']
        fargs = {'id': list_id, 'email': {'email': user_email}, 'delete_member': delete_member, 'send_goodbye': send_goodbye,
                 'send_notify': send_notify}

        return self.do('lists/unsubscribe', http_method='POST', content=self.build_content(fargs))
        # return self.check_response_success(res)
