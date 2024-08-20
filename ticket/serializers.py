from rest_framework import serializers,status
from rest_framework.exceptions import ValidationError
from django.core.validators import validate_email
import re
from django.contrib.auth import authenticate
from django.utils import timezone
from user_mgmt.models import RapifuzzUser
from .models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    incident_details = serializers.CharField(write_only=True)
    class Meta:
        model = Ticket
        exclude = ('incident_id','reporter')
        

    def validate_entity_type(self,value):
        if value.lower() not in ['enterprise','government']:
            raise ValidationError({"error":{"message":"Invalid Entity Selection"}})
        return value

    def validate_priority(self,value):
        if value.lower() not in ['low','medium','high']:
            raise ValidationError({"error":{"message":"Invalid Priority Selection"}})
        return value

    def validate_status(self,value):
        if value.lower() not in ['open','in progress','closed']:
            raise ValidationError({"error":{"message":"Invalid Priority Selection"}})
        return value

    def create(self, validated_data):
        ticket = self.Meta.model(**validated_data)
        ticket.reporter_id=self.context.get('request').user.id
        ticket.save()
        return ticket
    
    def update(self, instance, validated_data): 
        return super().update(instance, validated_data)