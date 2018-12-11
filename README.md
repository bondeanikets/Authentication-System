# Authentication System

RESTful API authentication system where we verify if a {user and password} combination matches with the ones stored in a database

## Getting Started

Unzip the folder, and make sure to have following packages and softwares installed:

### Prerequisites and Installation

Flask : ```pip install Flask```.
MongoDB on current machine : https://docs.mongodb.com/manual/installation/.
Flask-PyMongo : ```pip install Flask-PyMongo```.
Postman : https://www.getpostman.com/apps.

### Database

Start MongoDB instance by running ```mongod``` in a terminal, keep it running.

### Running the api

Open new terminal, go into "Authentication System" directory, and run the following command:

```python authentication.py```

Now you can use Postman to simulate requests. The OpenAPI format specification can be seen as specified below:

Go to: https://editor.swagger.io/, then clear the left editor.

Copy content of swagger.yaml from this directory to the link's editor, the right section shows all the possible paths.
Exploit Postman to simulate requests as given in the swagger document, and see the results!


### Reason for chosing MongoDB:

The current project specification doesn't really exploit the relational structure of relational databases, hence
a non-relational database was an obvious choice. Besides, MongoDB is easy to setup, highly scalable and good at 
handling dynamic querries. The scemaless feature of mongoDB is a bonus!

## Authors

* **Aniket Bonde**
