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

## Endpoints
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

## Creating Users
To create a new user, you first have to register them via the <i>registration</i> api.
To register a user, we send a request to `/api/auth/register` with the data in the following format:
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
There are two kinds of users in our backend, an <i> authuser </i> and a <i> CustomUser </i>.
Django handles user authentication via their own user model (located under django.contrib.auth.models.User).
Since Django handles user auth through a different model than we use to store user information, we have to somehow
match authusers with CustomUsers. This is done through the email field.

To create a new CustomUser, we send data to `/api/users/` in the following format:
```angular2html
data = {
    "firstName": [first name],
    "lastName": [last name],
    "email": [same email as authuser],
    ...
    (Additional CustomUser fields can be found 
    under board/models.py)
}
```
## Public User Endpoints
#### api/users/
Gives a list of all users.

Method: GET

Permissions: AllowAny (dev), IsSuperUser (prod)

#### api/users/[id]/
Returns user information with specific id.

Method: GET

Permissions: AllowAny (dev), IsSuperUser (prod)

## Public Startup Endpoints
#### api/startups/
Gives a list of all startups.

Method: GET

Permissions: AllowAny (dev), IsSuperUser (prod)

#### api/startups/[id]
Returns startup information given startup id.

Method: GET

Permissions: AllowAny (dev), IsSuperUser (prod)

## Public Listing Endpoints
#### api/listings/
Gives a list of all job listings.

Method: GET

Permissions: AllowAny (prod)

    search_fields = ['listName', 'listOrgID', 'listDesc']
    filterset_fields = ['listCategory', 'isPaid', 'listName', 'listOrgID', 'listDesc']

Searching: `/api/listings/?search=Business`

Filtering: `/api/listings/?isPaid=true`

#### api/listings/[id]/
Returns job listing information given listing id.

Method: GET

Permissions: AllowAny (prod)

#### api/listings/[id]/toggle/
Toggles a listing as bookmarked or not given a user's token.

Method: POST

Permissions: IsAuthenticated (prod)

#### api/listings/[id]/applicants/
Returns a list of applicants given a job listing id.

Method: GET

Permissions: AllowAny (prod)

#### api/listings/sort/[sort-key]/
Returns a sorted list of job listings based on search key.

#### api/listings/manage/[add/delete]
Adds or deletes a listing (for startups).

Method: POST or DELETE (depending on add or delete)

Permissions: IsAuthenticated, IsStartup (custom)

## Authorization Endpoints (no slash at end)
#### api/auth/user
Returns a user's information given Token (CustomUser and Startups).

Method: GET

Permissions: IsAuthenticated

#### api/auth/register
Registers a new authuser given username, email and password.

Method: POST

Permissions: AllowAny

#### api/auth/login
Logs a user in given username (email) and password.

Method: POST

Permissions: AllowAny

#### api/auth/logout
Logs a user out given token (invalidates user token).

Method: POST

Permissions: IsAuthenticated

#### api/auth/users/bookmarks/
Gets a query of Listing objects bookmarked by the user.

Method: GET

Permissions: IsAuthenticated

#### api/authusers/
Returns a list of current authusers.

Method: GET

Permissions: IsSuperUser

#### api/authusers/confirm/
Confirms if a user's password is valid.

Method: POST

Permissions: IsAuthenticated