# create domain
curl -s --request POST \
     --header "Accept: application/xml" \
     --header "Content-Type: application/xml;charset=UTF-8" \
     --data '<?xml version="1.0" encoding="UTF-8"?><taz:domainProperties xmlns:taz="http://authzforce.github.io/rest-api-model/xmlns/authz/5" />' \
     http://127.0.0.1:8080/authzforce-ce/domains

# List domain
curl -s --request GET http://127.0.0.1:8080/authzforce-ce/domains

# /domains/<id> to get specific domain data
