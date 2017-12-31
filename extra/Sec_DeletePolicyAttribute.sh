# Format: /policy/<policy_name>/<rule_name>/
curl http://127.0.0.1:8000/policy/NewTicketOnlySupport/NewTicket/ \
        --data-urlencode attribute_name="urn:oasis:names:tc:xacml:1.0:subject-category:access-subject" -u admin:Test1234 -X DELETE
