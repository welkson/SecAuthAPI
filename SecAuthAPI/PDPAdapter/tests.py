from wso2 import WSO2

# Authorization Services Config
as_product = 1     # 1- WSO2IS, 2-AuthZForce
as_api_url = 'https://localhost:9443/'
as_authtype = 1    # 1- Basic (user/password), 2- OAuth Token
as_user = 'admin'
as_password = 'admin'
as_token = ''

# policy test
p1 = """
    <Policy
        xmlns="urn:oasis:names:tc:xacml:3.0:core:schema:wd-17"  PolicyId="BloqueioAtaqueTest" RuleCombiningAlgId="urn:oasis:names:tc:xacml:3.0:rule-combining-algorithm:deny-overrides" Version="1.0">
        <Target>
            <AnyOf>
                <AllOf>
                    <Match MatchId="urn:oasis:names:tc:xacml:1.0:function:string-equal">
                        <AttributeValue DataType="http://www.w3.org/2001/XMLSchema#string">read</AttributeValue>
                        <AttributeDesignator AttributeId="urn:oasis:names:tc:xacml:1.0:action:action-id" Category="urn:oasis:names:tc:xacml:3.0:attribute-category:action" DataType="http://www.w3.org/2001/XMLSchema#string" MustBePresent="true"></AttributeDesignator>
                    </Match>
                </AllOf>
            </AnyOf>
        </Target>
        <Rule Effect="Permit" RuleId="permit"></Rule>
    </Policy>
"""

# Authorization Service Connection
pdp = WSO2(url=as_api_url,
           auth_type=as_authtype,
           user=as_user,
           password=as_password,
           token=as_token)

# Add new Policy
print u"Adding new policy..."
print pdp.create_policy(p1)

# List policies
print u"Listing policies..."
print pdp.get_policy()

# Remove Policy
print u"Removing policy..."
print pdp.delete_policy("BloqueioAtaqueTest")

print u"Tests OK!"
