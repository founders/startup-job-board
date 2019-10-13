from django.urls import path
from django.conf.urls import url, include

from . import views
from rest_framework import routers
from .views import UserViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    url("^", include(router.urls)),
    path('users/', views.ListUser.as_view()),
    path('users/<int:pk>/', views.DetailUser.as_view()),
]