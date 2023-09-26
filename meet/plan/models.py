import uuid
from django.conf import settings
from django.db import models


# Create your models here.
class Plan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    password = models.CharField(max_length=20, blank=True)
    title = models.CharField(max_length=50)
    time = models.DateTimeField()
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    memo = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"owner: {self.owner} , title: {self.title}"


class Group(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
