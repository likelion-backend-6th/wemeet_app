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
    def get(self,request):
        qs = Plan.objects.all()
        serializer = PlanSerializer(qs, many=True)
        return Response(serializer.data)
# Create your views here.

class PlanList(ListAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

# plan list 방법 3: 심플하지만 추상화 되어 있는 방법
class PlanViewSet(viewsets.ViewSet):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            name='title',
            in_=openapi.IN_PATH,
            description='약속 명',
            required=True,
            type=openapi.TYPE_STRING

        ),
        openapi.Parameter(
            name='time',
            in_=openapi.IN_PATH,
            description='약속 시간',
            required=True,
            type=openapi.TYPE_STRING

        )
    ])
    def list(self,request):
        queryset = Plan.objects.all()
        serializer = PlanSerializer(queryset, many=True)
        return Response(serializer.data)

    # uuid로 특정 plan get
    def retrieve(self, request, pk):
        queryset = Plan.objects.get(pk=pk)
        serializer = PlanSerializer(queryset)
        return Response(serializer.data)


class PlanViewSet2(ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


