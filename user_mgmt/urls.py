from django.urls import path
from .views import UserCreateView, index, UserLoginJWT

urlpatterns = [
    path('', UserCreateView.as_view(), name='user-create'),
    path('login/', UserLoginJWT.as_view(), name='user-login')
]
