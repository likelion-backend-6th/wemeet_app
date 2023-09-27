from django.shortcuts import render
from rest_framework import viewsets
from .serializers import PlanSerializer, GroupSerializer
from .models import Plan, Group


# Create your views here.
class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
