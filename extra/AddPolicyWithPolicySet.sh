curl http://127.0.0.1:8000/policy/ --data-urlencode name="NewTicketOnlySupport" --data-urlencode description="Only support role can register" --data-urlencode content@Policy/NewTicketOnlySupport_AZF.xml -u admin:Test1234

# AZF requires  PolicySetId="root" on PolicySet definitions
# Ref: https://github.com/authzforce/server/issues/15
