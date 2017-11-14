curl http://127.0.0.1:8000/policy/ --data-urlencode name="NewTicketOnlySupport" \
                                   --data-urlencode description="Only support role can register" \
                                   --data-urlencode content@Policy/NewTicketOnlySupport.xml \
                                   -u admin:Test1234

