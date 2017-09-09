curl --verbose --show-error --write-out '\n' --request GET \
    http://127.0.0.1:8080/authzforce-ce/domains/

echo "Fix domain id in AZF_Domain.txt"
