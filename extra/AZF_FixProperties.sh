curl --request "PUT" --header "Content-Type: application/xml;charset=UTF-8" \
     --data @Policy/AZF_FixProperties.xml --header "Accept: application/xml" \
     -vL \
     http://127.0.0.1:8080/authzforce-ce/domains/$(cat AZF_Domain.txt)/pap/pdp.properties
