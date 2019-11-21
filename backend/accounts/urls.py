from django.urls import path, include
from .api import RegisterAPI, LoginAPI, UserAPI, GetUserBookmarks, LoadHome
from knox import views as knox_views

urlpatterns = [
    path('api/auth', include('knox.urls')),
    path('api/auth/register', RegisterAPI.as_view()),
    path('api/auth/login', LoginAPI.as_view()),
    path('api/auth/user', UserAPI.as_view()),
    # path('api/auth/user/bookmarks', GetUserBookmarks.as_view()),
    path('api/auth/logout', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('', LoadHome.as_view())
]