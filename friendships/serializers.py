from rest_framework import serializers
from .models import FriendRequest
from user_mgmt.models import CustomUser  # Using the correct app name

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone_number', 'address', 'friends']

class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = CustomUserSerializer(read_only=True)
    to_user = CustomUserSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'timestamp', 'is_active']

class CreateFriendRequestSerializer(serializers.Serializer):
    to_user = serializers.IntegerField()

    def validate_to_user(self, value):
        try:
            CustomUser.objects.get(id=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User not found.")
        return value

class ActionSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['accept', 'decline'])

    def validate_action(self, value):
        if value not in ['accept', 'decline']:
            raise serializers.ValidationError("Invalid action.")
        return value