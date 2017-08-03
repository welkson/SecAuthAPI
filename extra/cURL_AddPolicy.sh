curl http://127.0.0.1:8000/policy/ --data-urlencode name="BloqueioTest" --data-urlencode description="PolicyTest1" --data-urlencode content@Policy/BloqueioTest.xml -u admin:Test1234

#curl http://127.0.0.1:8000/policy/ \                                         
#     --data-urlencode name="BloqueioTest" \
#     --data-urlencode description="PolicyTest1" \
#     --data-urlencode content@Policy/BloqueioTest.xml \    
#     -u admin:Test1234

# curl -v http://127.0.0.1:8000/policy/ -X POST -H 'Content-Type: application/json' -u admin:Test1234 -F content=@Policy/BloqueioTest.json

# curl -v http://127.0.0.1:8000/policy/ -X POST -H 'Content-Type: application/json' -u admin:Test1234 -d '{"name": "BloqueioTeste","description":"TestPolicy","content":"1234"}'
