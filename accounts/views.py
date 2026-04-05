from rest_framework import generics, permissions, viewsets
from .models import CustomUser
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, UserSerializer
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import generics
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType

# Registration
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


# Login
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "user": UserSerializer(user).data
            })
        return Response({"error": "Invalid credentials"}, status=400)


# Logout (delete token)
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"detail": "Successfully logged out."})
'''
# User ViewSet for profile management and follow/unfollow functionality
class UserViewSet(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def follow(self, request, pk=None):
        user_to_follow = get_object_or_404(CustomUser, pk=pk)
        if user_to_follow == request.user:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.add(user_to_follow)
        return Response({"detail": f"You are now following {user_to_follow.username}."}, status=status.HTTP_200_OK)

    def unfollow(self, request, pk=None):
        user_to_unfollow = get_object_or_404(CustomUser, pk=pk)
        if user_to_unfollow == request.user:
            return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.remove(user_to_unfollow)
        return Response({"detail": f"You have unfollowed {user_to_unfollow.username}."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def followers(self, request, pk=None):
        user = get_object_or_404(CustomUser, pk=pk)
        followers = user.followers.all()
        serializer = self.get_serializer(followers, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def following(self, request, pk=None):
        user = get_object_or_404(CustomUser, pk=pk)
        following = user.following.all()
        serializer = self.get_serializer(following, many=True)
        return Response(serializer.data)
    '''
        
    
class UserDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class FollowUserView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        user_to_follow = get_object_or_404(CustomUser, pk=user_id)
        if user_to_follow == request.user:
            return Response({"detail": "You cannot follow yourself."},
                            status=status.HTTP_400_BAD_REQUEST)

        request.user.following.add(user_to_follow)
        
        # Create notification
        Notification.objects.create(
            recipient=user_to_follow,
            actor=request.user,
            verb="followed you",
            target_content_type=ContentType.objects.get_for_model(CustomUser),
            target_object_id=request.user.id
        )

        return Response({"detail": f"You are now following {user_to_follow.username}."},
                        status=status.HTTP_200_OK)


class UnfollowUserView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        user_to_unfollow = get_object_or_404(CustomUser, pk=user_id)
        if user_to_unfollow == request.user:
            return Response({"detail": "You cannot unfollow yourself."},
                            status=status.HTTP_400_BAD_REQUEST)

        request.user.following.remove(user_to_unfollow)
        return Response({"detail": f"You have unfollowed {user_to_unfollow.username}."},
                        status=status.HTTP_200_OK)


class FollowersListView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        followers = user.followers.all()
        serializer = self.get_serializer(followers, many=True)
        return Response(serializer.data)


class FollowingListView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        following = user.following.all()
        serializer = self.get_serializer(following, many=True)
        return Response(serializer.data)
