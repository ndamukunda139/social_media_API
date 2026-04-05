from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FeedView, LikePostView, UnlikePostView
from rest_framework_nested import routers


# Main router 
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

# Nested router for comments under posts
post_router = routers.NestedDefaultRouter(router, r'posts', lookup='post')
post_router.register(r'comments', CommentViewSet, basename='post-comments')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(post_router.urls)),
    path('feed/', FeedView.as_view(), name='feed'),
    path('api-auth/', include('rest_framework.urls')),  # for browsable API login/logout

    # Like / Unlike endpoints
    path('posts/<int:pk>/like/', LikePostView.as_view(), name='like-post'),
    path('posts/<int:pk>/unlike/', UnlikePostView.as_view(), name='unlike-post'),
]

