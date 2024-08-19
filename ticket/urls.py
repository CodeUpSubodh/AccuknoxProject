from django.urls import path
from .views import TicketCreateView

urlpatterns = [
    path('', TicketCreateView.as_view(), name='create-ticket'),
]
