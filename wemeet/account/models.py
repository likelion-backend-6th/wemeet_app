from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(db_index=True, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.email
class UserLocation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    longitude = models.FloatField()  # 경도
    latitude = models.FloatField()   # 위도
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email}의 위치정보"