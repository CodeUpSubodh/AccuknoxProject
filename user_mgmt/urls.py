from django.urls import path
from .views import UserCreateView, index

urlpatterns = [
    path('', UserCreateView.as_view(), name='zenatixuser-create')
]
