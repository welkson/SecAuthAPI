# Format: /policy/<policy_name>/<rule_name>/<attribute_name>/
curl http://127.0.0.1:8000/policy/NewTicketOnlySupport/NewTicket/ \
        --data-urlencode attribute_name="http://wso2.org/claims/role" \
        --data-urlencode attribute_value="HyperAdmin" -u admin:Test1234 -X PUT
