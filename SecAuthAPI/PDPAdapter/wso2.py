from authservice import AuthService
from suds.client import Client
from SecAuthAPI import settings

# import logging

# ignore self-signed certificate errors
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# log
# logging.basicConfig(level=logging.INFO)
# logging.getLogger('suds.client').setLevel(logging.DEBUG)


class WSO2(AuthService):
    """ WSO2 Authorization Services """
    def __init__(self, *args, **kwargs):
        if 'url' in kwargs:
            # get conf from construct parameters
            self.url = kwargs.get('url')
            self.auth_type = kwargs.get('auth_type')
            self.user = kwargs.get('user')
            self.password = kwargs.get('password')
            self.token = kwargs.get('token')
        else:
            # get conf from settings.py
            self.url = settings.as_api_url
            self.auth_type = settings.as_authtype
            self.user = settings.as_user
            self.password = settings.as_password
            self.token = settings.as_token

    def connection(self):
        url_api = self.url + 'services/EntitlementPolicyAdminService?wsdl'
        client = Client(url_api, username=self.user, password=self.password)    # TODO: token

        return client

    def get_policy(self):
        # getAllPolicies parameters: policyTypeFilter, policySearchString, pageNumber, isPDPPolicy
        return self.connection().service.getAllPolicies("ALL", "*", 1, False).policySet   # TODO: standardize result

    def create_policy(self, name, content):
        client = self.connection()

        # TODO: capture namespace version automatically (e.g. 2337, 2340)
        policy_dto = client.factory.create("ax2340:PolicyDTO")  # DTO from WSDL Schema
        policy_dto.active = True
        policy_dto.policy = content
        policy_dto.promote = True   # TODO: test

        # import ipdb
        # ipdb.set_trace()

#       client.service.dePromotePolicy(name)

#       p = client.service.addPolicy(policy_dto)

#       client.service.publishToPDP(name, "CREATE", "1", True, "0")

        return client.service.addPolicy(policy_dto)

    def update_policy(self, content):
        client = self.connection()

        policy_dto = client.factory.create("ax2340:PolicyDTO")  # DTO from WSDL Schema
        policy_dto.active = True
        policy_dto.policy = content
        policy_dto.promote = True

        return client.service.updatePolicy(policy_dto)

    def delete_policy(self, name):
        self.connection().service.removePolicy(name, True)  # PolicyID, dePromote

        return True     # TODO: return error or successful result

# TODO: WSO2 apply police (refresh? restart service?)
