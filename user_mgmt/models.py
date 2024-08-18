from django.contrib.auth.models import AbstractUser
from django.db import models
from cities_light.models import City, Country
from django.contrib.auth.models import AbstractUser, Group, Permission, UserManager




class RapifuzzUserUserManager(UserManager):
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



class RapifuzzUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    pin_code = models.CharField(max_length=10)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    groups = models.ManyToManyField(
        Group,
        related_name="rapifuzzuser_set",  # Unique related_name for groups
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="rapifuzzuser_set",  # Unique related_name for permissions
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )
    def __str__(self):
        return self.email
