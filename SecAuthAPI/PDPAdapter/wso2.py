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
    """ WSO2 Authorization Services """
    def __init__(self, url, auth_type, user, password, token):
        self.url = url
        self.auth_type = auth_type
        self.user = user
        self.password = password
        self.token = token

    def connection(self):
        url_api = self.url + 'services/EntitlementPolicyAdminService?wsdl'
        client = Client(url_api, username=self.user, password=self.password)    # TODO: token
        return client

    def get_policy(self):
        # getAllPolicies parameters: policyTypeFilter, policySearchString, pageNumber, isPDPPolicy
        return self.connection().service.getAllPolicies("ALL", "*", 1, False).policySet   # TODO: standardize result

    def create_policy(self, content):
        client = self.connection()

        policy_dto = client.factory.create("ax2337:PolicyDTO")  # DTO from WSDL Schema
        policy_dto.active = True
        policy_dto.policy = content
        policy_dto.promote = True

        return client.service.addPolicy(policy_dto)

    def update_policy(self, content):
        client = self.connection()

        policy_dto = client.factory.create("ax2337:PolicyDTO")  # DTO from WSDL Schema
        policy_dto.active = True
        policy_dto.policy = content
        policy_dto.promote = True

        return client.service.updatePolicy(policy_dto)

    def delete_policy(self, name):
        self.connection().service.removePolicy(name, True)  # PolicyID, dePromote

        return True     # TODO: return error or successful result
