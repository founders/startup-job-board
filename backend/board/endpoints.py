from django.urls import path
from django.conf.urls import url, include

from . import views
from rest_framework import routers
from .views import UserViewSet, StartupViewSet, ListingViewSet

#from rest_framework.authtoken.views import obtain_auth_token  # <-- Here

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('startups', StartupViewSet)
router.register('listings', ListingViewSet)

urlpatterns = [
    url("^", include(router.urls)),
    path('users/', views.ListUser.as_view()),  # View all current users
    path('users/<int:pk>/', views.DetailUser.as_view()),  # Detail a user by their id
    path('users/<int:pk>/update/', views.UpdateUser.as_view()),  # Update user information
    path('authusers/', views.ListAuthUser.as_view()),  # View authenticated users
    path('startups/', views.ListStartup.as_view()),  # View all startups
    path('startups/<int:pk>/', views.DetailStartup.as_view()),  # View specific startups by id
    path('listings/', views.ListListing.as_view()),  # View all listings
    # path('listings/update/', views.UpdateListingsIsOpen.as_view()),
    path('listings/<int:pk>/', views.DetailListing.as_view()),  # View specific listings by id
    path('listings/<int:pk>/toggle/', views.ToggleListingToUser.as_view()),  # Toggle listings for users to bookmark
    path('listings/<int:pk>/applicants/', views.ViewUsersWhoApplied.as_view()),  # View applicants who applied to a position
    path('listings/sort/<str:order>/', views.ViewOrderedListings.as_view()),  # Sort listings by fields
    path('authusers/confirm/', views.ConfirmUserPassword.as_view())
    #path('auth/api-token-auth/', obtain_auth_token, name='api_token_auth'),
    # path('auth/login', views.login)
]