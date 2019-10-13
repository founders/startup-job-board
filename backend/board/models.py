# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=50)
    major = models.CharField(max_length=50)
    status = models.TextField()

    def __str__(self):
        """A string representation of our model"""
        return str(self.name) + " is a " + str(self.major) + " major."