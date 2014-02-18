from urllib import urlencode

from pyrate.main import Pyrate


class ConstantContactPyrate(Pyrate):
    # Get your OAUTH Token from:
    # https://constantcontact.mashery.com/apps/mykeys
    # request
    base_url = None  # see __init__
    default_header_content = None
    default_body_content = None
    auth_data = {'type': 'MANUAL'}
    send_json = True

    # response
    response_formats = []
    default_response_format = None
    validate_response = True

    connection_check = {'http_method': 'GET', 'target': 'account/info'}

    def __init__(self, api_key, token, default_response_format=None):
        super(ConstantContactPyrate, self).__init__()
        self.auth_data['api_key'] = api_key
        self.auth_data['token'] = token
        self.base_url = "https://api.constantcontact.com/v2/"
        self.default_header_content = {
            'Authorization': 'Bearer %s' % token
        }

        if default_response_format or default_response_format == '':
            self.default_response_format = default_response_format

    def request(self, method, target, content=None, request_headers=None, response_format=None, return_raw=False):

        # Appending api key to every request
        if '?' in target:
            target += '&'
        else:
            target += '?'

        target += "api_key=%s" % self.auth_data['api_key']
        return super(ConstantContactPyrate, self).request(
            method, target, content, request_headers, response_format, return_raw)

    def get_lists(self, modified_since=None):
        # modified_since in ISO-8601 eg: 2014-02-17T08:22:10+00:00
        target = 'lists'
        if modified_since:
            target += '?modified_since=%s' % urlencode(modified_since)

        return self.get(target)

    def get_list_by_id(self, id):
        lists = self.get_lists()
        for list in lists:
            if list['id'] == str(id):
                return list
        return None

    def get_list_by_name(self, name):
        lists = self.get_lists()
        for list in lists:
            if list['name'] == name:
                return list
        return None

    def create_contact(self, email, list_id, action_type):
        # action_type can be either ACTION_BY_OWNER or ACTION_BY_VISITOR
        target = 'contacts?action_by=%s' % action_type
        content = {
            'lists': [{'id': str(list_id)}],
            'email_addresses': [{'email_address': email}]
        }
        r = self.post(
            target=target,
            content=content,
            headers={"Content-Type": "application/json"},
            return_raw=True
        )

        success = False
        if r.status_code == 201:
            success = True
        return success, r.content

