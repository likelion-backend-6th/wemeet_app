from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.template.response import TemplateResponse
from django.views.generic import  ListView, DetailView


from .models import Plan, Group
from .serializers import PlanSerializer, GroupSerializer

class PlanViewSet(ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

    def list(self,request):
        qs = self.get_queryset()
        return TemplateResponse(request, 'plan/plan_list.html',{'qs':qs})

    def retrieve(self,request,pk):
        qs = self.get_queryset().get(pk=pk)
        return TemplateResponse(request, 'plan/plan_detail.html', {'qs':qs})
class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

######################## view ############################

class PlanList(ListView):
    model = Plan
    #template_name = 'plan/plan_list.html'
    context_object_name = 'plans'


class PlanDetail(DetailView):
    model = Plan
    context_object_name = 'plan'


