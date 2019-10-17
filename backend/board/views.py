# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import generics, viewsets, permissions

from .models import User, Startup, Listing
from .serializers import UserSerializer, StartupSerializer, ListingSerializer
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response

#
# @csrf_exempt
# @api_view(["POST"])
# @permission_classes((AllowAny,))
# def login(request):
#     username = request.data.get("username")
#     password = request.data.get("password")
#     if username is None or password is None:
#         return Response({'error': 'Please provide both username and password'},
#                         status=HTTP_400_BAD_REQUEST)
#     user = authenticate(username=username, password=password)
#     if not user:
#         return Response({'error': 'Invalid Credentials'},
#                         status=HTTP_404_NOT_FOUND)
#     token, _ = Token.objects.get_or_create(user=user)
#     return Response({'token': token.key},
#                     status=HTTP_200_OK)

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