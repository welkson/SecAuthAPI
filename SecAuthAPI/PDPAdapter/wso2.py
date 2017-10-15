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

    # workaround to fix bug in WSO2 PAP/PDP Cache
    # details:
    # https://stackoverflow.com/questions/46626886/bug-cache-in-wso2-pdp-when-policy-is-created-via-admin-services-api
    def clear_cache(self):
        url_admin_api = self.url + '/services/EntitlementAdminService?wsdl'
        client_admin_api = Client(url_admin_api, username=self.user, password=self.password)
        client_admin_api.service.clearPolicyCache()
        client_admin_api.service.clearDecisionCache()
        #
        # client_admin_api.service.refreshPolicyFinders()
        # client_admin_api.service.refreshResourceFinder()
        #
        # client_admin_api.service.clearAllAttributeCaches()
        # client_admin_api.service.clearAllResourceCaches()
        # client_admin_api.service.clearAttributeFinderCache()
        #
        # client_admin_api.service.clearCarbonAttributeCache()
        # client_admin_api.service.clearCarbonResourceCache()
        #
        return

    def get_policy(self):
        # getAllPolicies parameters: policyTypeFilter, policySearchString, pageNumber, isPDPPolicy
        return self.connection().service.getAllPolicies("ALL", "*", 1, False).policySet   # TODO: standardize result

    def create_policy(self, name, content):
        self.clear_cache()  # workaround to fix bug in PAP/PDP cache

        client = self.connection()

        # TODO: capture namespace version automatically (e.g. 2337, 2340)
        policy_dto = client.factory.create("ax2340:PolicyDTO")  # DTO from WSDL Schema
        policy_dto.active = True
        policy_dto.policy = content
        policy_dto.promote = True   # TODO: test
        policy = client.service.addPolicy(policy_dto)

        return policy

    def update_policy(self, content):
        client = self.connection()

        policy_dto = client.factory.create("ax2340:PolicyDTO")  # DTO from WSDL Schema
        policy_dto.active = True
        policy_dto.policy = content
        policy_dto.promote = True

        policy = client.service.updatePolicy(policy_dto)
        self.clear_cache()  # workaround to fix bug in PAP/PDP cache

        return policy

    def delete_policy(self, name):
        self.connection().service.removePolicy(name, True)  # PolicyID, dePromote
        self.clear_cache()  # workaround to fix bug in PAP/PDP cache

        return True     # TODO: return error or successful result
