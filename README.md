## Synopsis

This application is a generic Application Programming Interface (API) for manipulating access control policy based on Attribute-Based Access Control (ABAC). 
Our API follows a functional specification of ABAC, and aims to abstract away implementation details of access control 
engines, providing an effector that can be integrated into a self-adaptation approach.

Paper: 
Supporting the Self-adaptation of Authorization Infrastructures. Available from: https://www.researchgate.net/publication/321386327_Supporting_the_Self-adaptation_of_Authorization_Infrastructures [accessed Dec 31 2017].

## Motivation

Insiders pose a great threat to organizations due to their capacity of exploiting privileged access for inappropriate gain. 
Traditional access controlsolutions are not able to deal with insiders, and some solutions apply concepts of 
self-adaptation to handle such problems. Existing  work  has  been  focused on detecting or how to respond to a detected 
insider.  However, in order to allow the dynamic adaptation of access control policies, it is necessary to clearly
specify what modification actions can be applied to a policy.  Such actions can then be used for the definition of 
adaptation plans. 

## Installation

```
pip install -U -r requirements.txt
```


## Run SecAuthAPI

```
python manage.py runserver

at browser: http://127.0.0.1:8000 (API operations)
            http://127.0.0.1:8000/admin (Dashboard)
            http://127.0.0.1:8000/o/applications (OAuth register app)
```

## API Reference

See paper:
Supporting the Self-adaptation of Authorization Infrastructures. Available from: https://www.researchgate.net/publication/321386327_Supporting_the_Self-adaptation_of_Authorization_Infrastructures [accessed Dec 31 2017].


## Contributors

Welkson Medeiros <welkson.medeiros@ifrn.edu.br>

Carlos Eduardo da Silva <kaduardo@imd.ufrn.edu.br>

Diego Saraiva <diego.saraiva@ifrn.edu.br>


## License

The MIT License (MIT)