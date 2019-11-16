# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import generics, viewsets, permissions
from rest_framework import filters
from rest_framework.permissions import BasePermission

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from .models import CustomUser, Startup, Listing
from django.contrib.auth.models import User
from .serializers import CustomUserSerializer, StartupSerializer, ListingSerializer, UserSerializer
from django.contrib.auth.hashers import check_password

import json
import itertools

# Create your views here.

# Custom Permissions
class IsOwnerOrReadOnly(BasePermission):
    """
    Only be able to write to file if owner, otherwise grant read only permission.
    """
    def has_permission(self, request, view):
        # Always going to be true...
        print(view.kwargs)
        try:
            temp_user = CustomUser.objects.get(email=request.user.email)
            print(temp_user)
            return bool(view.kwargs['pk'] == CustomUser.objects.get(email=request.user.email).id)
        except:
            return False

class IsAbleToAdd(BasePermission):
    """
    Bad implementation but it works okay
    """
    message = "Listing ID is not valid."

    def has_permission(self, request, view):
        try:
            temp_user = CustomUser.objects.get(email=request.user.email)
            listing_index = view.kwargs['pk']
            listing_info = Listing.objects.get(id=listing_index).__str__()
            # Check for conversion to string
            if isinstance(temp_user.userBookmarks, str):
                temp_user.userBookmarks = {}
                temp_user.save()

            if not temp_user.userBookmarks.get(str(listing_index)):
                temp_user.userBookmarks[str(listing_index)] = listing_info
                temp_user.save()
                return True
            else:
                # Check if the listing is valid
                if (Listing.objects.filter(id=listing_index).exists()):
                    if temp_user.userBookmarks.get(str(listing_index)):
                        # If if already exists, remove it from the list
                        del temp_user.userBookmarks[str(listing_index)]
                        temp_user.save()
                        # print(temp_user.userBookmarks)
                        return True
                    #temp_user.userBookmarks['listings'] = temp_user.userBookmarks['listings'] + str("{}|".format(listing_index))
                    #temp_user.save()
                    return True
                return False
        except:
            return False

class IsStartup(BasePermission):
    """
    Checks to see if a currently signed in user is also a startup
    """
    message = "User's email does not match with any email belonging to Start-ups."
    def has_permission(self, request, view):
        return bool(Startup.objects.filter(orgEmail = request.user.email).count() > 0)

"""
User API
"""
class ListUser(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class DetailUser(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.AllowAny, ]
    serializer_class = CustomUserSerializer

class UpdateUser(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CustomUserSerializer

class ListAuthUser(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ConfirmUserPassword(generics.GenericAPIView):

    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        # print(request.data)
        isValid = check_password(request.data['password'], request.user.password)
        return Response({
            "isValid": isValid
        })

class AuthUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
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
    permission_classes = [permissions.AllowAny, ] # Change back to isAuthenticated later
    serializer_class = StartupSerializer

"""
Listing API
"""
class ListListing(generics.ListAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

class UpdateListingsIsOpen(generics.ListAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    for listing in queryset:
        listing.isOpen = listing.getIsOpen()
        listing.save()

class DetailListing(generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

class ToggleListingToUser(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated,
                          IsAbleToAdd]

    def post(self, request, *args, **kwargs):
        return Response({"status" : "okay",
                         "listing_toggled": kwargs['pk']})


class ListingUpdateView(generics.UpdateAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    permission_classes = [permissions.AllowAny, ]
    serializer_class = ListingSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['listName', 'listOrgID', 'listDesc']
    filterset_fields = ['listCategory', 'isPaid', 'listName', 'listOrgID', 'listDesc']


class ViewUsersWhoApplied(generics.ListAPIView):
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        # qs = super().get_queryset()
        # Return a queryset containing people who have a particular listings bookmarked
        # print(self.kwargs['pk'])
        return CustomUser.objects.filter(userBookmarks__has_key=str(self.kwargs['pk']))

class ViewOrderedListings(generics.ListAPIView):
    serializer_class = ListingSerializer

    def get_queryset(self):
        return Listing.objects.all().order_by(self.kwargs['order'])

# Sorting
# class SortByKeyword(generics.ListAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = ListingSerializer
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['listName', 'listOrg', 'listDesc']
