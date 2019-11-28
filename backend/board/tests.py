"""
API Testing for Users, Startups and Listings
"""

from django.test import TestCase
import requests
import random
import json
from .models import CustomUser, Startup, Listing

urlUser = "127.0.0.1:8000/api/users/"

class TestUserAPI(TestCase):
    @classmethod

    def setUp(cls):
        fnames = ["Davis", "Siraj", "Bobby", "Jordan"]
        lnames = ["Keene", "Chokshi", "Wang", "Campbell"]
        dobs = ["10-01-2000", "01-01-2000", "03-05-2001", "10-05-1997"]
        majors = ["CS", "BCOG", "CS", "Econ"]
        GPA = "4.0"
        Degree = "B.S"
        pitch = ["This is a test pitch."]
        extraCurriculars = [
            ["Yoyoing", "Tennis", "Programming"],
            ["Design", "Legos"],
            ["Money", "Computers", "Dropping Classes"],
            []

        ]
        bookmarks = [
            [],
            ["Apple, Inc."],
            ["Sentry.io", "Cruise"],
            ["Applebees", "Five Guys", "Wendys", "McDonalds"]
        ]
        for i in range(4):
            CustomUser.objects.create(firstName = fnames[i],
                                      lastName = lnames[i],
                                      dateOfBirth = dobs[i],
                                      authToken = str(random.randint(1234567890, 98765432100)),
                                      userMajor = majors[i],
                                      userGPA = GPA,
                                      userDegree = Degree,
                                      userPassword = str(random.randint(123456789, 9876543200)),
                                      userPitch = pitch,
                                      extraCurriculars = extraCurriculars[i],
                                      userBookmarks = bookmarks[i])

    def test_types(self):
        # check to see if all of our data went through
        allDataCount = CustomUser.objects.count()
        self.assertEqual(allDataCount, 4)

    def test_names(self):
        self.assertEqual(CustomUser.objects.get(id=1).firstName, "Davis")
        self.assertEqual(CustomUser.objects.get(id=2).firstName, "Siraj")
        self.assertEqual(CustomUser.objects.get(id=3).firstName, "Bobby")
        self.assertEqual(CustomUser.objects.get(id=4).firstName, "Jordan")
