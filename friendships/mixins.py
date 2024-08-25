from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.response import Response
from .models import FriendRequest

class RateLimitMixin:
    def check_rate_limit(self, user):
        # Define the time window (e.g., 1 minute)
        time_window = timedelta(minutes=1)
        # Get the current time
        now = datetime.now()
        # Calculate the time threshold
        time_threshold = now - time_window

        # Get the number of requests sent by the user in the last minute
        recent_requests = FriendRequest.objects.filter(
            from_user=user,
            timestamp__gte=time_threshold,
            is_active=True
        ).count()

        # Limit to 3 requests per minute
        if recent_requests >= 3:
            return False
        return True

    def create(self, request, *args, **kwargs):
        if not self.check_rate_limit(request.user):
            return Response(
                {"detail": "Rate limit exceeded. You can only send 3 friend requests per minute."},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        return super().create(request, *args, **kwargs)
