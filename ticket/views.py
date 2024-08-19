from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from .models import Ticket
from rest_framework import status
from rest_framework.response import Response
from user_mgmt.permissions import JwtAuthentication, IsAdvancedUser, IsBasicUser
from rest_framework.views import APIView
import jwt
from datetime import datetime, timedelta
from .serializers import TicketSerializer
def index(request):
    return HttpResponse("Welcome to the Ticket Management System!")

class TicketCreateView(generics.CreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    # permission_classes = [IsAdvancedUser | IsBasicUser]
    authentication_classes = [JwtAuthentication]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ticket=self.perform_create(serializer)
        ticket.save()
        data = {
            'status': 'success',
            'message': 'Ticket added successfully, verification pending',
            'ticket_id':ticket.incident_id,
            }
        return Response(data, status=status.HTTP_201_CREATED)
        
    def perform_create(self, serializer):
        return serializer.create(serializer.validated_data)
