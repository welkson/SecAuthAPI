from authservice import AuthService
from suds.client import Client
# import logging

# ignore self-signed certificate errors
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# log
# logging.basicConfig(level=logging.INFO)
# logging.getLogger('suds.client').setLevel(logging.DEBUG)


class WSO2(AuthService):
    """WSO2 Authorization Services"""
    def __init__(self, url, auth_type, user, password, token):
        self.url = url
        self.auth_type = auth_type
        self.user = user
        self.password = password
        self.token = token

    def connection(self):
        url_api = self.url + 'services/EntitlementPolicyAdminService?wsdl'
        client = Client(url_api, username=self.user, password=self.password)   # TODO: token
        return client

    def get_policy(self):
        # getAllPolicies parameters: policyTypeFilter, policySearchString, pageNumber, isPDPPolicy
        return self.connection().service.getAllPolicies("ALL", "*", 1, False)

    def create_policy(self, name, description, content):
        return NotImplemented

