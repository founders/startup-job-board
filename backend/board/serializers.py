from rest_framework import serializers
from .models import CustomUser, Startup, Listing
from django.contrib.auth.models import User
#Listing

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = User

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        # fields = (
        #     'id',
        #     'firstName',
        #     'lastName',
        #     'dateOfBirth',
        #     'authToken',
        #     'userMajor',
        #     'userGPA',
        #     'userDegree',
        #     'userPassword',
        #     'userPitch',
        #     'extraCurriculars',
        #     'userBookmarks'
        # )
        fields = '__all__'
        #extra_kwargs = {
        #    'userPassword': {'write_only': True},
        #}
        model = CustomUser

class StartupSerializer(serializers.ModelSerializer):
    class Meta:
        # fields = (
        #     'id',
        #     'orgName',
        #     'orgLocation',
        #     'orgListings',
        #     'orgDesc',
        #     'orgIndustry',
        #     'authToken',
        #     'orgPassword'
        # )
        fields = '__all__'
        #extra_kwargs = {
        #    'orgPassword' : {'write_only' : True},
        #}
        model = Startup

class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        # fields = (
        #     'id',
        #     'listName',
        #     'listDesc',
        #     'isPaid',
        #     'listLocation',
        #     'isOpen',
        #     'listLongDesc',
        #     'listOrgID'
        # )
        fields = '__all__'

        model = Listing