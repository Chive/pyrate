import imp
import requests

class Pyrate(object):

    def __init__(self, recipe):
        if recipe == '':
            raise Exception

        self.recipe = self.loadRecipe(recipe)
        #self.config = self.recipe.get_config()

    def loadRecipe(self, recipe):
        return imp.load_source(recipe, 'recipes/' + recipe + ".py")

    def get_oauth(self):
        return self.recipe.get_oauth()

    def check_connection(self):
        return self.do(self.recipe.API_CONNECTION_CHECK[0])

    def parse_method_template(self):
        return None

    def do(self, method, content=None, headers=None, http_method=None, return_format=None):

        request_body = self.recipe.DEFAULT_BODY_CONTENT
        if content is not None:
            request_body.update(content)

        request_headers = self.recipe.DEFAULT_HEADER_CONTENT
        if headers is not None:
            request_headers.update(headers)

        if http_method is None:
            http_method = self.recipe.DEFAULT_HTTP_METHOD

        if return_format is None:
            if self.recipe.DEFAULT_RETURN_FORMAT != '':
                return_format = "." + self.recipe.DEFAULT_RETURN_FORMAT
            else:
                return_format = ''

        request_url = self.recipe.BASE_URL + method + return_format
        request_headers = self.recipe.DEFAULT_HEADER_CONTENT
        request_body = self.recipe.DEFAULT_BODY_CONTENT

        return self.do_request(http_method, request_url, request_headers, request_body, return_format)

    def do_request(self, http_method, url, headers, body, return_format):

        if self.recipe.AUTH_TYPE == 'OAUTH1':
            auth_data = self.get_oauth()
        else:
            auth_data = None

        if http_method.upper() == 'GET':
            r = requests.get(url, headers=headers, auth=auth_data)

        elif http_method.upper() == 'POST':
            r = requests.get(url, params=body, headers=headers, auth=auth_data)

        elif http_method.upper() == 'PUT':
            r = requests.get(url, params=body, headers=headers, auth=auth_data)

        elif http_method.upper() == 'DELETE':
            r = requests.get(url, params=body, headers=headers, auth=auth_data)

        elif http_method.upper() == 'OPTIONS':
            r = requests.get(url, params=body, headers=headers, auth=auth_data)

        print r

        return self.handle_response(r, return_format)

    def handle_response(self, response, return_format):
        try:
            return response.json()
        except Exception:
            return response.content
        return response.content