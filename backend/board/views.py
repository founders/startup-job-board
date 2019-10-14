# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import generics, viewsets, permissions

from .models import User, Startup, Listing
from .serializers import UserSerializer, StartupSerializer, ListingSerializer

# Create your views here.

"""
User API
"""
class ListUser(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class DetailUser(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny, ]
    serializer_class = UserSerializer

"""
Startup API
"""
class ListStartup(generics.ListAPIView):
    queryset = Startup.objects.all()
    serializer_class = StartupSerializer

class DetailStartup(generics.RetrieveUpdateDestroyAPIView):
    queryset = Startup.objects.all()
    serializer_class = StartupSerializer

class StartupViewSet(viewsets.ModelViewSet):
    queryset = Startup.objects.all()
    permission_classes = [permissions.AllowAny, ]
    serializer_class = StartupSerializer

"""
Listing API
"""
class ListListing(generics.ListAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

class DetailListing(generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    permission_classes = [permissions.AllowAny, ]
    serializer_class = ListingSerializer