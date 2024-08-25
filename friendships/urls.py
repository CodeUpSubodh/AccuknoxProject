from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FriendRequestViewSet

# Create a router and register the viewset
router = DefaultRouter()
router.register(r'friend-requests', FriendRequestViewSet, basename='friendrequest')

# Define the URL patterns
urlpatterns = [
    path('', include(router.urls)),
]
