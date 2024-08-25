from rest_framework import serializers,status
from .models import CustomUser
from rest_framework.exceptions import ValidationError
from django.core.validators import validate_email
import re
from django.contrib.auth import authenticate
from django.utils import timezone
import jwt

def _is_valid_phone(phone_number):
        pattern = re.compile(r'^\+[0-9]+-[0-9]+$')
        if pattern.match(phone_number):
            return True
        else:
            return False

class GenerateJwtSerialiser(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        request = self.context.get('request')
        email = attrs.get('email')
        password = attrs.get('password')
        print(password)
        if email and password:
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                msg = ("User does not exist")
                raise serializers.ValidationError(msg)
            authenticate=user.check_password(password)
            if authenticate:
                if not user.is_active:
                    msg = ('User account is disabled.')
                    raise serializers.ValidationError(msg)
            else:
                msg = ('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = ('Must include "username" and "password" .')
            raise serializers.ValidationError(msg)
        attrs['user'] = user
        return attrs



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ('username',)
        

    def validate_phone_number(self,value):
        phone_numbers = CustomUser.objects.values_list('phone_number',flat=True)
        if not _is_valid_phone(value):
            raise ValidationError({"error":{"message":"Please enter a valid phone number to continue"}})
        if len(value) < 12:
            raise ValidationError({"error":{"message":"Please enter a valid phone number to continue"}})
        if self.instance is None and value in phone_numbers:
            raise ValidationError({"error":{"message":"Phone number already present, please enter a different one"}})
        # Check for uniqueness during update
        if self.instance and value != self.instance.phone_number and value in phone_numbers:
            raise ValidationError({"error":{"message":"Phone number already present, please enter a different one"}})
        return value

    def validate_email(self,value):
        emails = CustomUser.objects.values_list('email',flat=True)
        try:
            validate_email(value.lower())
        except:
            ValidationError({"error":{"message":"Please enter a valid email to continue"}})       
        if value == '':
            raise ValidationError({"error":{"message":"This field may not be blank."}}) 
        if self.instance is None and value.lower() in emails:
            raise ValidationError({"error":{"message":"Email already present, please enter a different one"}})
        # Check for uniqueness during update
        if self.instance and value.lower() != self.instance.email and value.lower() in emails:
            raise ValidationError({"error":{"message":"Email already present, please enter a different one"}})

        return value.lower()

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        validated_data['username'] = validated_data['email']
        user = self.Meta.model(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data): 
        validated_data['username'] = validated_data['email']
        return super().update(instance, validated_data)