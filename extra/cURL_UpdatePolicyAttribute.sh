# Format: /policy/<policy_name>/<rule_name>/<attribute_name>/
curl http://127.0.0.1:8000/policy/RegistrationOnlyAdmin/Registration/role/ \
        --data-urlencode attribute_value="SuperAdmin" -u admin:Test1234 -X PUT
