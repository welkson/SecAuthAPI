curl http://127.0.0.1:8000/policy/ --data-urlencode name="RegistrationOnlyAdmin" --data-urlencode description="Only admin can register" --data-urlencode content@Policy/RegistrationOnlyAdmin.xml -u admin:Test1234

