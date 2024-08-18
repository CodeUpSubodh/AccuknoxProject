from django.contrib import admin
from .models import RapifuzzUser

@admin.register(RapifuzzUser)
class RapifuzzUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'phone_number')  # Adjust fields as needed
