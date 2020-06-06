"""
API Testing for Users, Startups and Listings
"""

from django.test import TestCase
import requests
import random
import json

url = 'http://127.0.0.1:8000/api/users/'
headers = {'content-type': 'application/json'}

def test_get_user():
    r = requests.get(url, headers=headers)
    print(r.json())

def test_post_user():
    data = {
        "firstName": "Davis",
        "lastName": "Keene",
        "dateOfBirth": "1971-01-01",
        "authToken": "000000001",
        "userMajor": "CS",
        "userGPA": "4.0",
        "userDegree": "B.S",
        "userPassword": "root",
        "userPitch": "I am a student.",
    }
    r = requests.post(url, headers=headers, data=json.dumps(data))

test_post_user()
