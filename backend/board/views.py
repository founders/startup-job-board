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
    message = 'User already has listing bookmarked, or internal error.'

    def has_permission(self, request, view):
        try:
            temp_user = CustomUser.objects.get(email=request.user.email)
            listing_index = view.kwargs['pk']
            # Check for conversion to string
            if isinstance(temp_user.userBookmarks, str):
                temp_user.userBookmarks = {}
                temp_user.save()
            if not temp_user.userBookmarks.get('listings'):
                temp_user.userBookmarks['listings'] = "|{}|".format(listing_index)
                temp_user.save()
                return True
            else:
                # Check if the listing is valid
                if (Listing.objects.filter(id=listing_index).exists()):
                    if str(listing_index) in temp_user.userBookmarks['listings']:
                        # If if already exists, remove it from the list
                        temp_str = temp_user.userBookmarks['listings'].replace(str(listing_index), '')
                        # print(temp_str)
                        temp_str = ''.join(i for i, _ in itertools.groupby(temp_str))
                        temp_user.userBookmarks['listings'] = temp_str
                        temp_user.save()
                        # print(temp_user.userBookmarks)
                        return True
                    temp_user.userBookmarks['listings'] = temp_user.userBookmarks['listings'] + str("{}|".format(listing_index))
                    temp_user.save()
                    return True
                return False
        except Exception as e:
            print(e)
            return False


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
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = StartupSerializer

"""
Listing API
"""
class ListListing(generics.ListAPIView):
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
    #
    # def update(self, request, *args, **kwargs):
    #     queryset = Listing.objects.all()
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = serializer.validated_data
    #     # If this user doesn't have any bookmarked listings
    #     if not user.userBookmarks.get("listings"):
    #         user.userBookmarks['listings'] = list(request.data['id'])
    #     else :
    #         user.userBookmarks['listings'].append(request.data['id'])
    #
    #     return super(ListingUpdateView, self).update(request, *args, **kwargs)

    # def post(self, request):
    #     queryset = Listing.objects.all()
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = serializer.validated_data
    #     listing = ListingSerializer(queryset, many=True)
    #     if not user.userBookmarks:
    #         user.userBookmarks['listings'] = list(listing.data['id'])
    #         return Response({
    #             'status': '200'
    #         })
    #     elif user.userBookmarks :
    #         user.userBookmarks['listings'].append(listing.data['id'])
    #         return Response({
    #             'status': '200'
    #         })
    #     else:
    #         return Response({
    #             'status': '400'
    #         })


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    permission_classes = [permissions.AllowAny, ]
    serializer_class = ListingSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['listName', 'listOrgID', 'listDesc']
    filterset_fields = ['listCategory', 'isPaid', 'listName', 'listOrgID', 'listDesc']




# Sorting
# class SortByKeyword(generics.ListAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = ListingSerializer
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['listName', 'listOrg', 'listDesc']
