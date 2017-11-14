import cStringIO
import requests
from authservice import AuthService
from SecAuthAPI import settings


class AuthZForce(AuthService):
    """AuthZForce Authorization Services"""
    def __init__(self, *args, **kwargs):
        if 'url' in kwargs:
            # get conf from construct parameters
            self.url = kwargs.get('url')
            self.auth_type = kwargs.get('auth_type')
            self.user = kwargs.get('user')
            self.password = kwargs.get('password')
            self.token = kwargs.get('token')
            self.domain = kwargs.get('domain')
        else:
            # get conf from settings.py
            self.url = settings.as_api_url
            self.auth_type = settings.as_authtype
            self.user = settings.as_user
            self.password = settings.as_password
            self.token = settings.as_token
            self.domain = settings.as_domain

    def connection(self):
        return NotImplemented

    def create_policy(self, name, content):
        url_azf_api = "%s/domains/%s/pap/policies" % (self.url, self.domain)

        headers = {'Accept': 'application/xml',
                   'Content-Type': 'application/xml;charset=UTF-8'}

        # TODO: policy has policyset?

        response = requests.post(url_azf_api, headers=headers, data=content, verify=False)

        # TODO: remove debug
        print "<-------  AZF Response --------> \n", response.text

        # TODO: define return pattern

        return response

    def get_policy(self):
        return NotImplemented

    def delete_policy(self):
        raise NotImplementedError

    def update_policy(self):
        raise NotImplementedError
