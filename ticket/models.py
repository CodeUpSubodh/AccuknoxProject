from django.db import models
from django.utils import timezone
import random
import string
from user_mgmt.models import RapifuzzUser

class Ticket(models.Model):
    # ENTERPRISE = 'Enterprise'
    # GOVERNMENT = 'Government'
    # ENTITY_CHOICES = [
    #     (ENTERPRISE, 'Enterprise'),
    #     (GOVERNMENT, 'Government'),
    # ]

    # HIGH = 'High'
    # MEDIUM = 'Medium'
    # LOW = 'Low'
    # PRIORITY_CHOICES = [
    #     (HIGH, 'High'),
    #     (MEDIUM, 'Medium'),
    #     (LOW, 'Low'),
    # ]

    # OPEN = 'Open'
    # IN_PROGRESS = 'In Progress'
    # CLOSED = 'Closed'
    # STATUS_CHOICES = [
    #     (OPEN, 'Open'),
    #     (IN_PROGRESS, 'In Progress'),
    #     (CLOSED, 'Closed'),
    # ]

    incident_id = models.CharField(max_length=20, unique=True, editable=False)
    entity_type = models.CharField(max_length=20)
    reporter = models.ForeignKey(RapifuzzUser, on_delete=models.CASCADE)
    incident_details = models.TextField()
    reported_date_time = models.DateTimeField(default=timezone.now)
    priority = models.CharField(max_length=10)
    status = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        if not self.incident_id:
            self.incident_id = self.generate_incident_id()
        super().save(*args, **kwargs)

    def generate_incident_id(self):
        current_year = timezone.now().year
        random_number = ''.join(random.choices(string.digits, k=5))
        return f"RMG{random_number}{current_year}"

    def __str__(self):
        return self.incident_id
