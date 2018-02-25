curl -H "Authorization: Bearer S760bVdDhxNDhAW4PNs0aDKOeQvrqT" http://127.0.0.1:8000/policy/ --data-urlencode name="NewTicketOnlySupport" \
                                   --data-urlencode description="Only support role can register" \
                                   --data-urlencode content@Policy/NewTicketOnlySupport.xml

# for register application and get access token:
# https://django-oauth-toolkit.readthedocs.io/en/latest/rest-framework/getting_started.html#step-3-register-an-application
