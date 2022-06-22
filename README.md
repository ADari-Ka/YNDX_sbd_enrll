# Yandex School of Backend Development enrollment


### Architecture
In a **root directory** there are important for launch files:
- Dockerfile & docker-compose.yaml (and compose files for testing)
- requirements.txt (used libraries and their versions)
- ignore files (.gitignore and .dockerignore)
- README.md with instructions

**Folder "tests"** contains the following types of tests: end-to-end and unit. Also, in e2e there are another Dockerfile and requirements files for launching end-to-end tests.

**Web_app** has all server files in child directories with _config.py_ file. 

You also can see here the layers' division:
- ***model/*** is a folder with business domain model classes _(model had been described due all OpenAPI specification file)_
- ***adapters/*** contains special features for database interface
- ***service/*** is a service-layered functions which are connecting entrypoints with database
- ***entrypoints/*** the web-server itself: handlers of request's.

### Launch 
To run wep-app with PostgreSQL database you can launch Docker containers **via Docker-compose** 

Use this command in your terminal *(in case you launch Docker deamon under sudo access, be sure to startup your containers with the same rights)*:


    docker-compouse up --build

By default, on your machine you can access to web-server by http://127.0.0.1:8080

**BUT** hosted version for enrollment has _80_ port instead _8080_

### Testing
#### All tests were made with pytest library
You can run ***unit tests***, please use this command:
    
    docker-compose -f docker-compose.yaml -f dc-unit-tests.yaml up --build --abort-on-container-exit

They cover the key functions:
- Hand-made parser work
- Method *to_dict()* of Node (OfferAndCategory) class
- Creating node object form the json data (with validations)

You can run ***end-to-end tests***, please use this command:
    
    docker-compose -f docker-compose.yaml -f dc-e2e-tests.yaml up --build --abort-on-container-exit

They can also contain integration part of testing as well

Covered features are:
- Import nodes (adding new and update exist)
- Get node's information
- Delete node (with children if they exist)
- Get sales info
- Get statistic about the node
- Errors catching


### Author - Kalashnikova Daria 
> Student in Innopolis University, 1st year bachelor 

You can contact me on Telegram [@ADari-Ka](https://t.me/ADari_Ka) or by [e-mail](ADari.Ka@yandex.ru) :)