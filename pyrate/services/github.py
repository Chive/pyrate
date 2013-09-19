from pyrate.main import Pyrate


class OrganisationNotFoundError(Exception):
    pass


class GithubPyrate(Pyrate):
    # These variables must be set on instantiation
    auth_user = ''
    auth_pass = ''

    http_methods = ['GET', 'POST', 'PATCH', 'DELETE']
    return_formats = []
    default_body_content = {}
    auth_type = 'BASIC_AUTH'
    connection_check_method = ('GET', '#')
    base_url = 'https://api.github.com/'
    send_json = True

    def __init__(self, auth_user, auth_pass, default_http_method=None, default_return_format=None):
        super(GithubPyrate, self).__init__()
        self.auth_user = auth_user
        self.auth_pass = auth_pass
        self.default_header_content = {
            'Authorization': self.create_basic_auth(self.auth_user, self.auth_pass)
        }

        if default_http_method:
            self.default_http_method = default_http_method

        if default_return_format or default_return_format == '':
            self.default_return_format = default_return_format

    def get_my_orgs(self):
        return self.do('user/orgs', http_method='GET')

    def create_repo(self, name, description=False, org_name=False, private=False):
        fargs = {'name': name, 'description': description, 'private': private}
        if org_name:
            query = 'orgs/' + str(org_name) + '/repos'
        else:
            query = 'user/repos'

        return self.do(query, http_method='POST', content=self.build_content(fargs))

    def delete_repo(self, name, org_name=False):
        if org_name:
            user = str(org_name)
        else:
            user = self.auth_user

        query = 'repos/' + user + '/' + name
        return self.do(query, http_method='DELETE')
