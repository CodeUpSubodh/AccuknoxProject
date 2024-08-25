from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, UserManager




class CustomUserUserManager(UserManager):
    def create_user(self,username ,email, password, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email)
        
        user.is_superuser = extra_fields['is_superuser']
        user.is_active = extra_fields['is_active']
            
        user.set_password(password)
        user.save()
        return user

        
    def create_superuser(self, username,email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(username,email, password, **extra_fields)



class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    friends = models.ManyToManyField('self', blank=True)
    groups = models.ManyToManyField(
        Group,
        related_name="CustomUser_set",  # Unique related_name for groups
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="CustomUser_set",  # Unique related_name for permissions
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )
    def __str__(self):
        return self.email

    def send_friend_request(self, user):
        if not FriendRequest.objects.filter(from_user=self, to_user=user).exists():
            friend_request = FriendRequest(from_user=self, to_user=user)
            friend_request.save()

    def accept_friend_request(self, friend_request):
        if friend_request.to_user == self:
            friend_request.accept()

    def decline_friend_request(self, friend_request):
        if friend_request.to_user == self:
            friend_request.decline()

    def cancel_friend_request(self, friend_request):
        if friend_request.from_user == self:
            friend_request.cancel()