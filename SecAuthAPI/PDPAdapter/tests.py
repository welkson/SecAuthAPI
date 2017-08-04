from wso2 import WSO2

as_product = 1     # 1- WSO2IS, 2-AuthZForce
as_api_url = 'https://localhost:9443/'
as_authtype = 1    # 1- Basic (user/password), 2- OAuth Token
as_user = 'admin'
as_password = 'admin'
as_token = ''

pdp = WSO2(url=as_api_url,
           auth_type=as_authtype,
           user=as_user,
           password=as_password,
           token=as_token)

print pdp.get_policy()
