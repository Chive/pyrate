from pyrate.main import Pyrate
from pyrate.utils import clean_dict


class OrganisationNotFoundError(Exception):
    pass


class GithubPyrate(Pyrate):

    # request
    base_url = 'https://api.github.com/'
    default_header_content = None  # see __init__
    default_body_content = None
    auth_data = {'type': 'BASIC'}
    send_json = True

    # response
    response_formats = []
    default_response_format = None
    validate_response = True

    connection_check = {'http_method': 'GET', 'target': '#'}

    def __init__(self, auth_user, auth_pass):
        super(GithubPyrate, self).__init__()
        self.auth_data['username'] = auth_user
        self.auth_data['password'] = auth_pass
        self.default_header_content = {
            'Authorization': self.get_auth_data()
        }

    def get_my_orgs(self):
        return self.get('user/orgs')

    def create_repo(self, name, description=False, org_name=False, private=False):
        kwargs = clean_dict({'name': name, 'description': description,
                             'private': private})
        if org_name:
            target = 'orgs/%s/repos' % str(org_name)
        else:
            target = 'user/repos'

        return self.post(target, content=kwargs)

    def delete_repo(self, name, org_name=False):
        if org_name:
            user = str(org_name)
        else:
            user = self.auth_data['user']

        return self.delete('repos/%s/%s' % (user, name))
