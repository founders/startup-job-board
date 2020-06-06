from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from board.models import CustomUser, Startup, Listing
from board.serializers import CustomUserSerializer, ListingSerializer, StartupSerializer
from django.contrib.auth.models import User


# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1],
            "is_startup": bool(Startup.objects.filter(orgEmail=user.email).count() > 0)
        })


# Login API
class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1],
            "is_startup": bool(Startup.objects.filter(orgEmail=user.email).count() > 0)
        })


# Get User API
class UserAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.AllowAny,
    ]

    # serializer_class = CustomUserSerializer
    def get_serializer_class(self):
        if Startup.objects.filter(orgEmail=self.request.user.email).count() > 0:
            return StartupSerializer
        elif CustomUser.objects.filter(email=self.request.user.email).count() > 0:
            return CustomUserSerializer

    def get_object(self):
        # If the authuser is a user
        if (CustomUser.objects.filter(email=self.request.user.email).count() > 0):
            return CustomUser.objects.get(email=self.request.user.email)
        elif (Startup.objects.filter(orgEmail=self.request.user.email).count() > 0):
            return Startup.objects.get(orgEmail=self.request.user.email)
    # return self.request.user

class GetUserBookmarks(generics.GenericAPIView):
  serializer_class = ListingSerializer
  permission_classes = [permissions.IsAuthenticated, ]

  def get(self, request):
    user = CustomUser.objects.filter(email=request.user.email)
    bookmarked_ids = user.userBookmarks.keys()
    return Listing.objects.filter(id__in=bookmarked_ids)

class LoadHome(generics.GenericAPIView):
    def get(self, request):
        return Response({
            "status": 200
        })
