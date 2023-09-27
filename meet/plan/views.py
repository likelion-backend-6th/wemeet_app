from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Plan, Group
from .serializers import PlanSerializer, GroupSerializer


class PlanListAPI(APIView):
    def get(self, request):
        qs = Plan.objects.all()
        serializer = PlanSerializer(qs, many=True)
        return Response(serializer.data)


# Create your views here.
