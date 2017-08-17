from SecAuthAPI.PDPAdapter.wso2 import WSO2
from SecAuthAPI import settings


class Adapter:
    @staticmethod
    def add_policy(name, description, content):
        print "<<<<<<<< AS EM USO: ", settings.as_product
        if settings.as_product == 1:                                     # WSO2 (TODO: constants?)
            # Add new Policy
            return WSO2().create_policy(content)

        elif settings.as_product == 2:                                  # AuthZForce
            return NotImplemented

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
