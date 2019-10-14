from django.urls import path
from django.conf.urls import url, include

from . import views
from rest_framework import routers
from .views import UserViewSet, StartupViewSet, ListingViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('startups', StartupViewSet)
router.register('listings', ListingViewSet)

urlpatterns = [
    url("^", include(router.urls)),
    path('users/', views.ListUser.as_view()),
    path('users/<int:pk>/', views.DetailUser.as_view()),
    path('startups/', views.ListStartup.as_view()),
    path('startups/<int:pk>/', views.DetailStartup.as_view()),
    path('listings/', views.ListListing.as_view()),
    path('listings/<int:pk>/', views.DetailListing.as_view())
]