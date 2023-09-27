from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from .models import Plan
from .serializers import PlanSerializer


# Create your views here.
class PlanList(ListAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

