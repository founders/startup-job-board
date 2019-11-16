# API Documentation

Founders Backend API Documentation.

## Getting Started Locally
Make sure that you have all of the proper requirements for the server to run locally by running:
pip3 install -r requirements.txt

Second, get the config.py file (for founders sql password) from here:
https://drive.google.com/open?id=1puDFEjLAIqN8htaCIl-daZ-jFtVkx3RU
and put it in backend/backend/ (where settings.py, wsgi.py and urls.py are located).

Run the server my navigating to the backend directory and running:
python3 manage.py runserver

Assuming everything goes well, you should see the server up and running on
localhost:8000

##Endpoints
This API currently has three endpoints:
/api/users, /api/startups, and /api/listings

## Making a request from the server
Assuming that the server is up and running, making a request is as easy as using curl or requests in python:
```angular2html
# Get Request
import requests

url = 'http://127.0.0.1:8000/api/users'
headers = {'content-type': 'application/json'}
r = requests.get(url, headers=headers)

# Post Request (add, delete)

data = {
    "firstName": "First",
    "lastName": "Last",
    "dateOfBirth": "1970-01-01",
    "authToken": "000000001",
    "userMajor": "CS",
    "userGPA": "4.0",
    "userDegree": "B.S",
    "userPassword": "root",
    "userPitch": "I am a student.",
}
r = requests.post(url, headers=headers, data=json.dumps(data))
 
```
# Docs
[Creating Users](#creating-users)

## Creating Users
To create a new user, you first have to register them via the <i>registration</i> api.
To register a user, send a request with the data in the following format:
```angular2html
email = "example@gmail.com"
data = {
    "username": email,
    "email": email,
    "password": "your-password"
}
```
The following response should be in this format:
```angular2html
{
    "user": {
        "id": [user id],
        "username": [user email]
        "email": [also user email]
    },
    "token": "[user auth token]",
    "is_startup": [Boolean, true if authuser is a startup.]
}
```