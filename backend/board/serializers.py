from rest_framework import serializers
from .models import User, Startup, Listing
#Listing

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'firstName',
            'lastName',
            'dateOfBirth',
            'authToken',
            'userMajor',
            'userGPA',
            'userDegree',
            'userPassword',
            'userPitch',
            'extraCurriculars',
            'userBookmarks'
        )
        extra_kwargs = {
            'userPassword': {'write_only': True},
        }
        model = User

class StartupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'orgName',
            'orgLocation',
            'orgListings',
            'orgDesc',
            'orgIndustry',
            'authToken',
            'orgPassword'
        )
        extra_kwargs = {
            'orgPassword' : {'write_only' : True},
        }
        model = Startup

class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'listName',
            'listDesc',
            'isPaid',
            'listLocation',
            'isOpen',
            'listLongDesc'
        )

        model = Listing