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

class TicketCreateView(generics.RetrieveUpdateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    # permission_classes = [IsAdvancedUser | IsBasicUser]
    authentication_classes = [JwtAuthentication]

    def post(self, request, *args, **kwargs):
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

    def get(self, request, *args, **kwargs):
        """Handles GET request to view a ticket."""
        ticket_id = kwargs.get('pk')
        try:
            ticket=Ticket.objects.get(id=ticket_id)
        except:
            return Response({'error':'Ticket Does Not Exsist'})
        data = {
            'entity_type': ticket.entity_type,
            'priority': ticket.priority,
            'status': ticket.status,
            'details': ticket.incident_details,
            'ticket_id':ticket.incident_id
            }
        return Response(data, status=status.HTTP_200_OK)