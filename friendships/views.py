from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import get_authorization_header
from user_mgmt.permissions import JwtAuthentication  # Import your JWT authentication class
from .models import FriendRequest
from .serializers import FriendRequestSerializer, CreateFriendRequestSerializer, ActionSerializer
from user_mgmt.models import CustomUser  # Using the correct app name
from .mixins import RateLimitMixin

class FriendRequestViewSet(RateLimitMixin,viewsets.ModelViewSet):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    authentication_classes = [JwtAuthentication]

    def list(self, request, *args, **kwargs):
        # Filter friend requests related to the authenticated user
        user = request.user
        friend_requests = FriendRequest.objects.filter(
            from_user=user
        ) | FriendRequest.objects.filter(
            to_user=user
        )
        serializer = self.get_serializer(friend_requests, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = CreateFriendRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        to_user_id = serializer.validated_data['to_user']
        try:
            to_user = CustomUser.objects.get(id=to_user_id)
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if from_user == to_user:
            return Response({"detail": "You cannot send a friend request to yourself."}, status=status.HTTP_400_BAD_REQUEST)

        if to_user in from_user.friends.all() or from_user in to_user.friends.all():
            return Response({"detail": "You are already friends."}, status=status.HTTP_400_BAD_REQUEST)

        if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
            return Response({"detail": "Friend request already sent."}, status=status.HTTP_400_BAD_REQUEST)

        friend_request = FriendRequest(from_user=from_user, to_user=to_user)
        friend_request.save()
        return Response({"detail": "Friend request sent.","id": friend_request.id}, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        friend_request = self.get_object()
        serializer = ActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        action = serializer.validated_data['action']
        if friend_request.from_user==request.user:
            if 'accept' in action:
                friend_request.accept()
                return Response({"detail": "Friend request accepted.","id": friend_request.id}, status=status.HTTP_200_OK)
            elif 'decline' in action:
                friend_request.decline()
                return Response({"detail": "Friend request declined.","id": friend_request.id}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid action."})

    def destroy(self, request, pk=None):
        friend_request = self.get_object()
        if friend_request.from_user == request.user:
            friend_request.cancel()
            return Response({"detail": "Friend request canceled.","id": friend_request.id}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "You cannot cancel this friend request."}, status=status.HTTP_403_FORBIDDEN)
