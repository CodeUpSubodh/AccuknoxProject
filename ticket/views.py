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
            'message': 'Ticket added successfully',
            'ticket_id':ticket.incident_id,
            }
        return Response(data, status=status.HTTP_201_CREATED)
        
    def perform_create(self, serializer):
        return serializer.create(serializer.validated_data)

    def get(self, request, *args, **kwargs):
        ticket_id = kwargs.get('pk')
        try:
            ticket=Ticket.objects.get(id=ticket_id)
        except:
            return Response({'error':'Ticket Does Not Exsist'})
        request_data_user = self.request.user
        print(request_data_user)
        print(ticket.reporter)
        if request_data_user.id == ticket.reporter.id:
            data = {
                'entity_type': ticket.entity_type,
                'priority': ticket.priority,
                'status': ticket.status,
                'details': ticket.incident_details,
                'ticket_id':ticket.incident_id
             }
            return Response(data, status=status.HTTP_200_OK)
        else:
                return Response({"error": "No permission to view the ticket"})

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        ticket_id = kwargs.get('pk')
        ticket=Ticket.objects.get(id=ticket_id)
        request_data_user = self.request.user
        if request_data_user.id == ticket.reporter.id:
            data = {
                'status': 'success',
                'message': 'Ticket updated successfully',
                'ticket_id': instance.incident_id,
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
                return Response({"error": "No permission to edit this ticket"})


class UserTicketListView(generics.ListAPIView):
    authentication_classes = [JwtAuthentication]

    def get_queryset(self):
        user = self.request.user
        return Ticket.objects.filter(reporter=user)

    def get(self, request, *args, **kwargs):
        tickets = self.get_queryset()
        data = []
        for ticket in tickets:
            data.append({
                'id': ticket.id,
                'ticket_id': ticket.incident_id,  # Assuming `incident_id` is a unique identifier
                'entity_type': ticket.entity_type,
                'priority': ticket.priority,
                'status': ticket.status,
                'details': ticket.incident_details,  # Ensure this is included
                'incident_id': ticket.incident_id,
                'reporter': ticket.reporter.username  # Adjust based on your reporter field
            })

        return Response(data)