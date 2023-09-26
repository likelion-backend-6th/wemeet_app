from django.db import models
from django.contrib.auth.models import User

class UserLocation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    longitude = models.FloatField()  # 경도
    latitude = models.FloatField()   # 위도
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email}의 위치정보"