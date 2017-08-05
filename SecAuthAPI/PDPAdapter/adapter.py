from django.conf import settings

from SecAuthAPI.PDPAdapter.wso2 import WSO2


class Adapter:
    @staticmethod
    def add_policy(name, description, content):
        if settings.as_product == 1:                                     # WSO2 (TODO: constants?)
            # Authorization Service Connection
            pdp = WSO2(url=settings.as_api_url,                          # TODO: singleton?
                       auth_type=settings.as_authtype,
                       user=settings.as_user,
                       password=settings.as_password,
                       token=settings.as_token)

            # Add new Policy
            return pdp.create_policy(content)
