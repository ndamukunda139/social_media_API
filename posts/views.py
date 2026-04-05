from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import NotFound
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework import filters
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Post, Like
from .serializers import PostSerializer
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType




# Custom permission: only allow owners to edit/delete
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read-only permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only for the owner of the post/comment
        return obj.author == request.user
    
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    # Filtering and searching
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['content']  # allow searching by post content
    ordering_fields = ['created_at']  # allow ordering by date

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['content']
    ordering_fields = ['created_at', 'author__username']

    def get_queryset(self):
        post_id = self.kwargs.get('post_pk')
        queryset = Comment.objects.all().order_by('-created_at')
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        author_id = self.request.query_params.get('author')
        if author_id:
            queryset = queryset.filter(author_id=author_id)
        return queryset

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_pk')
        post = get_object_or_404(Post, pk=post_id)
        comment = serializer.save(author=self.request.user, post=post)

        # Notify post author
        if post.author != self.request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=self.request.user,
                verb="commented on your post",
                target_content_type=ContentType.objects.get_for_model(comment.__class__),
                target_object_id=comment.id
            )


class FeedView(generics.GenericAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Get all users the current user is following
        following_users = request.user.following.all()

        # Get posts authored by those users
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')

        # Serialize and return
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)


class LikePostView(generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        # ✅ Safely fetch post
        post = get_object_or_404(Post, pk=pk)

        # ✅ Create like if not exists
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            return Response({"detail": "You already liked this post."},
                            status=status.HTTP_400_BAD_REQUEST)

        # ✅ Create notification for post author
        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb="liked your post",
                target_content_type=ContentType.objects.get_for_model(Post),
                target_object_id=post.id
            )

        return Response({"detail": "Post liked successfully."},
                        status=status.HTTP_201_CREATED)


class UnlikePostView(generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        # ✅ Safely fetch post
        post = generics.get_object_or_404(Post, pk=pk)

        # ✅ Find existing like
        like = Like.objects.filter(user=request.user, post=post).first()
        if not like:
            return Response({"detail": "You have not liked this post."},
                            status=status.HTTP_400_BAD_REQUEST)

        like.delete()
        return Response({"detail": "Post unliked successfully."},
                        status=status.HTTP_200_OK)

