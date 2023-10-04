from django.conf import settings
from django.db import models


class UserLocation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    latitude = models.CharField(blank=True, null=True, max_length=50) #위도
    longitude = models.CharField(blank=True, null=True, max_length=50) #경도
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}의 위치정보"
