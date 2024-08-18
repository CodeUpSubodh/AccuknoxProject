from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from .models import RapifuzzUser
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserSerializer, GenerateJwtSerialiser
from .permissions import JwtAuthentication, IsAdvancedUser
from rest_framework.views import APIView
def index(request):
    return HttpResponse("Welcome to the USer Management System!")


class UserCreateView(generics.CreateAPIView):
    queryset = RapifuzzUser.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAdvancedUser]
    # authentication_classes = [JwtAuthentication]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=self.perform_create(serializer)
        print(user)
        user.save()
        data = {
            'status': 'success',
            'message': 'User added successfully, verification pending',
            'user_id':user.id,
            'username':user.username,
            'source':'admin'
            
            }
        return Response(data, status=status.HTTP_201_CREATED)
        
    def perform_create(self, serializer):
        return serializer.create(serializer.validated_data)

class UserLoginJWT(APIView):
     def post(self, request, *args, **kwargs):
        user_id = request.data.get("email",None)
        serializer = GenerateJwtSerialiser(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        encoded_token = jwt.encode(
            {'user_id': user.id, 'exp': datetime.utcnow() + timedelta(hours=14)}, JWT_KEY)
        response = dict()
        response['token'] = encoded_token
        return Response(response,status=status.HTTP_200_OK)
