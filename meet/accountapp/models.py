from django.conf import settings
from django.db import models

from django_prometheus.models import ExportModelOperationsMixin


class UserLocation(ExportModelOperationsMixin("location"), models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    latitude = models.CharField(blank=True, null=True, max_length=50)  # 위도
    longitude = models.CharField(blank=True, null=True, max_length=50)  # 경도
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}의 위치정보"

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(blank=True,null=True, upload_to = 'uploads/%Y/%m/%d/')
    message = models.CharField(max_length=250, blank=True, null=True)