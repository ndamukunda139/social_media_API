from django.urls import path
from .views import (
    UserDetailView,
    FollowUserView,
    UnfollowUserView,
    FollowersListView,
    FollowingListView,
)

urlpatterns = [
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'),
    path('users/<int:pk>/followers/', FollowersListView.as_view(), name='user-followers'),
    path('users/<int:pk>/following/', FollowingListView.as_view(), name='user-following'),
]


'''
from django.urls import path, include
from rest_framework import routers
from .views import RegisterView, LoginView, LogoutView, UserDetailView, FollowUserView, UnfollowUserView, FollowersListView, FollowingListView
from rest_framework_simplejwt.views import TokenRefreshView

routers = routers.DefaultRouter()
routers.register(r'', UserDetailView, basename='user')  # Registering the UserDetailView for user-related endpoints

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    #
    path('', include('rest_framework.urls')),  # for browsable API login/logout
    path('', include(routers.urls)),

    # User detail
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),

    # Follow / Unfollow endpoints
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'),

    # Followers / Following lists
    path('users/<int:pk>/followers/', FollowersListView.as_view(), name='user-followers'),
    path('users/<int:pk>/following/', FollowingListView.as_view(), name='user-following'),
]
'''