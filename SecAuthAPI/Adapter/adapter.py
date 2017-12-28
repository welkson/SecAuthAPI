from SecAuthAPI.Adapter.wso2 import WSO2
from SecAuthAPI.Adapter.authzforce import AuthZForce
from SecAuthAPI import settings
from SecAuthAPI.Core.xacml import Xacml


class Adapter:
    @staticmethod
    def create_policy(name, description, content):
        if settings.as_product == 1:                                    # WSO2 (TODO: constants?)
            # Add new Policy
            return WSO2().create_policy(name, content)

        elif settings.as_product == 2:                                  # AuthZForce
            return AuthZForce().create_policy(name, content)

        else:
            return None

    @staticmethod
    def delete_policy(name):
        if settings.as_product == 1:                                     # WSO2 (TODO: constants?)
            # Delete Policy
            return WSO2().delete_policy(name)

        elif settings.as_product == 2:                                  # AuthZForce
            return NotImplemented

        else:
            return None

    @staticmethod
    def update_policy(name, description, content):
        if settings.as_product == 1:                                     # WSO2 (TODO: constants?)
            # Update Policy
            return WSO2().update_policy(content)

        elif settings.as_product == 2:                                  # AuthZForce
            return NotImplemented

        else:
            return None

    @staticmethod
    def get_policy(name):
        return NotImplemented

    @staticmethod
    def clear_cache():
        if settings.as_product == 1:                                     # WSO2 (TODO: constants?)
            # Clear PAP/PDP cache
            return WSO2().clear_cache()
