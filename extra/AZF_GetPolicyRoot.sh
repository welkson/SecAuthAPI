curl --verbose --show-error --write-out '\n' --request GET \
    http://127.0.0.1:8080/authzforce-ce/domains/$(cat AZF_Domain.txt)/pap/policies/root/latest
