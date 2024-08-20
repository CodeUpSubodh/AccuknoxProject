from django.urls import path
from .views import TicketCreateView, UserTicketListView

urlpatterns = [
    path('', TicketCreateView.as_view(), name='create-ticket'),
    path('<int:pk>/', TicketCreateView.as_view(), name='ticket-detail'),
    path('tickets/', UserTicketListView.as_view(), name='user-tickets')
]
