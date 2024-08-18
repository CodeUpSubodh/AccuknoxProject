from rest_framework import permissions
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from jwt import decode, ExpiredSignatureError, InvalidTokenError
from django.conf import settings
from .models import RapifuzzUser

JWT_KEY = 'MIICXQIBAAKBgQCJ2+HrfX5w2caQwQalxE4WBUrA+SbZFCoLGJU71GFIfVqUVhgF'

class IsBasicUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow Basic users to view only
        if request.user.is_staff:
            return True
        
        for instance in request.user.permission_group.all():
            if instance.permissions.filter(codename="can_view_configurations_user").exists():
                return True
        return False


class IsAdvancedUser(permissions.BasePermission):
    def has_permission(self, request, view):
        
        # Allow Advance users to view, create Basic and Intermediate users
        for instance in request.user.permission_group.all():
            if instance.permissions.filter(codename="can_view_configurations_user").exists() and instance.permissions.filter(codename="can_edit_configurations_user").exists() and instance.permissions.filter(codename="can_add_configurations_user").exists() and instance.permissions.filter(codename="can_enable_configurations_user").exists() and instance.permissions.filter(codename="can_disable_configurations_user").exists() and instance.permissions.filter(codename="can_create_admin_users").exists():
                return True
        return False

class JwtAuthentication(BaseAuthentication):
    def authenticate(self, request):
        
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise AuthenticationFailed('Please provide token')

        token = auth_header.split(' ')[1]

        try:
            payload = decode(token, JWT_KEY, algorithms='HS256')
            user = RapifuzzUser.objects.get(pk=int(payload['user_id']))
            if not user.is_active:
                    raise jwt.ExpiredSignatureError()
            return user, None
        except ExpiredSignatureError:
            raise AuthenticationFailed('Signature expired. Please log in again.')
        except InvalidTokenError:
            raise AuthenticationFailed('Invalid token. Please log in again.')
        except RapifuzzUser.DoesNotExist:
            raise AuthenticationFailed('Some problem occurred in validating data.')

    def authenticate_header(self, request):
        return 'Bearer'
