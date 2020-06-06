# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import generics, viewsets, permissions
from rest_framework import filters
from rest_framework.permissions import BasePermission
# from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseNotFound
# from rest_framework.exceptions import MethodNotAllowed, PermissionDenied, NotFound
# from rest_framework.views import exception_handler
from rest_framework import status

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
    Bad implementation but it works, okay?
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

class IsListingOwner(BasePermission):
    message = "User is not a startup, or does not have permission to access this job listing."
    def has_permission(self, request, view):
        email = request.user.email
        startup = Startup.objects.filter(orgEmail=email)
        return bool(str(view.kwargs['pk']) in startup[0].orgListings)

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

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['firstName', 'lastName', 'userGradYear', 'userDegree', 'userMajor', 'email']
    filterset_fields = {'id': ['gte', 'lte', 'exact'], 'firstName': [],
                        'userGPA' : ['gte', 'lte'], 'lastName' : [],
                        'userGradYear' : ['gte', 'lte'], 'userDegree' : [],
                        'userMajor':[], 'email':[]}

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

class GetUserBookmarks(generics.ListAPIView):
    # serializer_class = ListingSerializer
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        user = CustomUser.objects.filter(email=self.request.user.email)[0]
        bookmarked_ids = user.userBookmarks.keys()
        queryset = Listing.objects.filter(id__in=bookmarked_ids)
        return queryset


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

# class UpdateListingsIsOpen(generics.ListAPIView):
#     queryset = Listing.objects.all()
#     serializer_class = ListingSerializer
#     for listing in queryset:
#         listing.isOpen = listing.getIsOpen()
#         listing.save()

class DetailListing(generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

class ToggleListingToUser(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated,
                          IsAbleToAdd]

    def post(self, request, *args, **kwargs):
        user = CustomUser.objects.filter(email=request.user.email)[0]

        return Response({"status" : "okay",
                         "listingToggled": kwargs['pk'],
                         "isBookmarked": bool(user.userBookmarks.get(str(kwargs['pk'])))})


class ListingUpdateView(generics.UpdateAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsListingOwner
    ]

class ToggleListingFromStartup(generics.GenericAPIView):
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsStartup]

    def post(self, request, *args, **kwargs):
        email = request.user.email
        startup = Startup.objects.filter(orgEmail=email)[0]
        # Add organization id to the request data
        request.data['listOrgID'] = startup.id
        # Serialize the listing
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        listing = serializer.save()
        new_listing = ListingSerializer(listing, context=self.get_serializer_context()).data
        # Save the listing to the startup
        startup.orgListings[str(new_listing['id'])] = listing.listDesc
        startup.save()

        return Response({
            "listing": new_listing,
        }, status=status.HTTP_200_OK)

    def delete(self, request):
        try:
            email = request.user.email
            startup = Startup.objects.filter(orgEmail=email)[0]
            listing = Listing.objects.filter(id=request.data['id'])[0]
            new_listing = ListingSerializer(listing, context=self.get_serializer_context()).data
            if startup.orgListings.get(str(request.data['id'])):  # If the listing belongs to the startup
                del startup.orgListings[str(request.data['id'])]
                startup.save()
                listing.delete()

                return Response({
                    "listing": new_listing
                })
            else:
                return Response({
                    "message": "Listing does not belong to this startup!"
                }, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({
                "A listing with this ID does not exist!"
            }, status=status.HTTP_404_NOT_FOUND)


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    permission_classes = [permissions.AllowAny, ]
    serializer_class = ListingSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['listName', 'listOrgID', 'listDesc']
    filterset_fields = ['listCategory', 'isPaid', 'listName', 'listOrgID', 'listDesc']


class ViewUsersWhoApplied(generics.ListAPIView):
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        # qs = super().get_queryset()
        # Return a queryset containing people who have a particular listings bookmarked
        # print(self.kwargs['pk'])
        return CustomUser.objects.filter(userBookmarks__has_key=str(self.kwargs['pk']))