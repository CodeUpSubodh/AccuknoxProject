from rest_framework import serializers,status
from .models import RapifuzzUser
from rest_framework.exceptions import ValidationError
from django.core.validators import validate_email
import re
from django.contrib.auth import authenticate
from django.utils import timezone
from cities_light.models import City, Country
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
                user = RapifuzzUser.objects.get(email=email)
            except RapifuzzUser.DoesNotExist:
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
    country = serializers.CharField(write_only=True)
    city = serializers.CharField(write_only=True)
    pin_code = serializers.CharField(write_only=True)
    class Meta:
        model = RapifuzzUser
        exclude = ('username',)
        

    def validate_phone_number(self,value):
        phone_numbers = RapifuzzUser.objects.values_list('phone_number',flat=True)
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
        emails = RapifuzzUser.objects.values_list('email',flat=True)
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

    def validate_country(self,value):
        try:
            country=Country.objects.get(name=value)
        except Country.DoesNotExist:
            raise ValidationError({"error":{"message":"Please entery a Valid Country to Proceed"}})
        return country

    def validate_city(self,value):
        try:
            city=City.objects.get(name=value)
            print(city)
        except City.DoesNotExist:
            raise ValidationError({"error":{"message":"Please entery a Valid City to Proceed"}})
        return city

    def validate_pin_code(self, value):
        try:
            city = City.objects.get(geoname_id=value)
            print(city)
            print("pincode")
        except City.DoesNotExist:
            raise ValidationError({"error": {"message": "Please enter a valid pincode to proceed"}})

        country = self.initial_data.get('country')
        city_name = self.initial_data.get('city')
        if city_name and country:
            if city.name != city_name or city.country.name != country:
                raise ValidationError({"error": {"message": "Pincode does not match the provided city and country"}})
        return value

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