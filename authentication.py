from flask import Flask, request, jsonify
import json
import uuid
import hashlib
from flask_pymongo import PyMongo

app = Flask(__name__)
DB_NAME='signup'
app.config["MONGO_URI"] = "mongodb://localhost:27017/" + DB_NAME
mongo = PyMongo(app)

@app.route("/")
def main_page():
    return('Welcome to Signup App')


@app.route("/login", methods=['POST'])
def login():
    credentials = request.get_json(force=True)
    password_check_bool = check_password(get_from_db({'username':credentials['username']})['password'], credentials['password'])
    retrieved_data = get_from_db({'username':credentials['username']})
    if password_check_bool and retrieved_data:
        return ("You are logged in!")
    else:
        return ("Incorrect Username or Password")

@app.route("/signup", methods=['POST'])
def signup_page():
    credentials = request.get_json(force=True)
    validate_bool, errors = validate(credentials)
    same_existing_username = get_from_db(query={'username':credentials['username']})
    if validate_bool and not same_existing_username:
        credentials['password'] = hash_password(credentials['password'])
        save_to_db(credentials)
        return ('Signup Data Saved Succesfully')
    elif same_existing_username:
        return ("Same username is already present in the database")
    else:
        return ("Invalid Signup Data. " + ', '.join(errors))


@app.route("/signup", methods=['PUT'])
def update_signup_data():
    credentials = request.get_json(force=True)
    # Checks if stored hashed password is same as the password in the body when hashed
    password_check_bool = check_password(get_from_db({'username':credentials['username']})['password'], 
    credentials['current_password'])
    if password_check_bool:
        update_data_in_db(credentials)
        return ("Credentials Updated Successfully")
    else:
        return ("Credentials NOT Updated, improper username or password")

    

@app.route("/signup", methods=['DELETE'])
def delete_signup_data():
    credentials = request.get_json(force=True)
    # Checks if stored hashed password is same as the password in the body when hashed
    password_check_bool = check_password(get_from_db({'username':credentials['username']})['password'], credentials['password'])
    if password_check_bool:
        remove_from_db({'username':credentials['username']})
        return ("Credentials Deleted Successfully")
    else:
        return ("Credentials NOT Deleted, improper username or password")


################################# HELPER FUNCTIONS #####################################

def hash_password(password):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt
    
def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

def validate(credentials):
    errors = []
    for field in ['username', 'password']:
        if field not in credentials:
            errors.append(field + ' not present in request data')
    return ('username' in credentials and 'password' in credentials and not errors), errors




################################# DATABASE FUNCTIONS #####################################

def get_from_db(query):
    retrieved_data = mongo.db.login_credentials.find_one(query)
    return retrieved_data

def save_to_db(credentials):
    mongo.db.login_credentials.insert(credentials)
    return

def update_data_in_db(credentials):
    query = {"username": credentials['username']}
    update = {"$set": {"password": hash_password(credentials['new_password'])}}
    mongo.db.login_credentials.update_one(query, update)
    return

def remove_from_db(credentials):
    mongo.db.login_credentials.remove(credentials)
    return


if __name__ == '__main__':
    app.run()

