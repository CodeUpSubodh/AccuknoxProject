from rest_framework import permissions
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from jwt import decode, ExpiredSignatureError, InvalidTokenError
from django.conf import settings
from .models import CustomUser

JWT_KEY = 'MIICXQIBAAKBgQCJ2+HrfX5w2caQwQalxE4WBUrA+SbZFCoLGJU71GFIfVqUVhgF'

class JwtAuthentication(BaseAuthentication):
    def authenticate(self, request):
        
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise AuthenticationFailed('Please provide token')

        token = auth_header.split(' ')[1]

        try:
            payload = decode(token, JWT_KEY, algorithms='HS256')
            user = CustomUser.objects.get(pk=int(payload['user_id']))
            if not user.is_active:
                    raise jwt.ExpiredSignatureError()
            return user, None
        except ExpiredSignatureError:
            raise AuthenticationFailed('Signature expired. Please log in again.')
        except InvalidTokenError:
            raise AuthenticationFailed('Invalid token. Please log in again.')
        except CustomUser.DoesNotExist:
            raise AuthenticationFailed('Some problem occurred in validating data.')

    def authenticate_header(self, request):
        return 'Bearer'
