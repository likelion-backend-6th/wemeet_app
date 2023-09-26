from django.db import models
from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(db_index=True, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.email

class UserLocation(models.Model):
    location_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    longitude = models.FloatField()  # 경도
    latitude = models.FloatField()   # 위도
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email}의 위치정보"