import requests
import json
import random

url = 'http://127.0.0.1:8000/api/listings/'
headers = {'content-type': 'application/json'}
# r = requests.get(url, headers=headers)

# Post Request (add, delete)

CATEGORIES = [
    "ANY",
    "Accounting",
    "Finance"
    "Agriculture",
    "Art",
    "Design",
    "Project Management",
    "Software Engineering"
]

NAMES = [
    "ANY",
    "Business Consultant",
    "Stock Exchange Analyst",
    "Farming Specialist",
    "Photographer",
    "UX Intern",
    "Robotics Project Manager",
    "Software Engineer",
]

for i in range(0, len(NAMES)-1):
    data = {
        "listName": NAMES[i],
        "listCategory": CATEGORIES[i],
        "listDesc": "This is a short description.",
        "isPaid": random.choice([True, False]),
        "listLocation": "Urbana, IL",
        "listLongDesc": "This is a slightly longer description, including credentials and requirements.",
        "listOrgID": random.randint(0, len(NAMES))
    }
    r = requests.post(url, headers=headers, data=json.dumps(data))
