# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django_mysql.models import JSONField
from django.contrib import admin
from django import forms
import datetime

# Create your models here.

class CustomUser(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    dateOfBirth = models.CharField(max_length=50)
    authToken = models.CharField(max_length=100)
    userMajor = models.CharField(max_length=100)
    userGPA = models.CharField(max_length=10)
    userDegree = models.CharField(max_length=100)
    userPassword = models.CharField(max_length=100)
    userPitch = models.CharField(max_length=300)
    extraCurriculars = JSONField(default=dict)
    userBookmarks = JSONField(default=dict)

    def __str__(self):
        """A string representation of a User"""
        return str(self.firstName) + " is a " + str(self.userMajor) + " major."

    def addBookmark(self, listing):
        self.userBookmarks.append(listing)

class Listing(models.Model):
    listName = models.CharField(max_length=50)
    listCategory = models.CharField(max_length=50)
    listDesc = models.CharField(max_length=250)
    isPaid = models.BooleanField(default= True)
    listLocation = models.CharField(max_length=100)
    isOpen = models.BooleanField(default= True)
    listLongDesc = models.TextField()
    listOrgID = models.CharField(max_length=100, default="")

    def __str__(self):
        """A string representation of a Job Listing"""
        return str(self.listName) + " is a " + str(self.listTag) + " listing."

    def setIsPaid(self, boolean):
        self.isPaid = boolean
        super(Listing, self).save()

class Startup(models.Model):
    orgName = models.CharField(max_length=50)
    orgLocation = models.CharField(max_length=100)
    orgListings = JSONField(default=dict)
    orgDesc = models.CharField(max_length=300)
    orgIndustry = models.CharField(max_length=100)
    authToken = models.CharField(max_length=100, default="")
    orgPassword = models.CharField(max_length=100, default="")

    def __str__(self):
        """A string representation of a Startup"""
        return str(self.orgName) + " is a " + str(self.orgIndustry) + " company."

    def addListing(self, listing):
        self.orgListings.append(listing)