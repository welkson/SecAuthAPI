# TODO: use FixProperties! Tem que informar na regra root qual o policyset da regra para avaliação
curl --request "POST" --header "Content-Type: application/xml;charset=UTF-8" \
     --data @Policy/AZF_Root_DenyAll.xml --header "Accept: application/xml" \
     -vL \
     http://127.0.0.1:8080/authzforce-ce/domains/$(cat AZF_Domain.txt)/pap/policies

# OBS: AZF use internal Policy "root" with Permit-All! It is necessary overwrite default policy to Deny
