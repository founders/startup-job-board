# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .models import User

class UserModelTest(TestCase):

    @classmethod

    def setUpTestData(cls):
        User.objects.create(name='Siraj Chokshi')
        User.objects.create(major="BCOG")

    def test_name(self):
        user = User.objects.get(id=1)
        expect_name = f'{user.name}'
        self.assertEqual(expect_name, "Siraj Chokshi")

    def test_major(self):
        user = User.objects.get(id=2)
        expect_major = f'{user.major}'
        self.assertEqual(expect_major, "BCOG")

# Create your tests here.
