from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

class FriendRequest(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_friend_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_friend_requests', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.from_user} -> {self.to_user}"

    def accept(self):
        self.to_user.friends.add(self.from_user)
        self.from_user.friends.add(self.to_user)
        self.is_active = False
        self.save()

    def decline(self):
        self.is_active = False
        self.save()

    def cancel(self):
        self.is_active = False
        self.save()
