import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import requests
from django.core.serializers import serialize
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.template.response import TemplateResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import PlanForm
from .models import Plan, Group
from .serializers import PlanSerializer, GroupSerializer
from account.models import UserLocation


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
    paginate_by = '6'

class PlanDetail(DetailView):
    model = Plan
    context_object_name = 'plan'
    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        #해당 아이템의 id값
        plan_id = self.kwargs['pk']
        #해당 Plan에 참여한 유저 리스
        context['group'] = Group.objects.filter(plan=plan_id)
        context['is_member'] = Group.objects.filter(plan=plan_id, user=self.request.user).exists()
        return context


@login_required()
def plan_create(request):
    if request.method == 'POST':
        form = PlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.owner = request.user

            ## kakao map -> 주소지에서 위도 경도 추출해서 저장하기 ##
            url = 'https://dapi.kakao.com/v2/local/search/address.json?query={address}'.format(address=plan.address)
            headers = {"Authorization": "KakaoAK " + '33e22754a9930e9cb1e0ab6f691bd8d0'}
            response = json.loads(str(requests.get(url, headers=headers).text))
            geodata = response.json() if isinstance(response, requests.models.Response) else response
            #print(geodata)
            if geodata:
                plan.latitude = geodata['documents'][0]['y']
                plan.longitude = geodata['documents'][0]['x']

            plan.save()
            return redirect('plan')

    else:
        form=PlanForm()
        return render(request, 'plan/plan_form.html',{'form':form})

@login_required
def plan_edit(request,pk):
    #수정할 plan
    plan = get_object_or_404(Plan, pk=pk)

    #작성자 아닌경우
    if request.user != plan.owner:
        return redirect('plan')

    if request.method == 'POST':
        form = PlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            return redirect('plan')
    else:
        form = PlanForm(instance=plan)

    return render(request, 'plan/plan_form.html', {'form':form})



@login_required
def plan_delete(request,pk):
    plan = get_object_or_404(Plan, pk=pk)
    if plan.owner == request.user:
        plan.delete()
    else:
        return reverse('plan')

    return redirect('plan')

@login_required
def group_create(request, pk):
    plan = get_object_or_404(Plan, pk=pk)
    # Check if the user is already a member of the group.
    if not Group.objects.filter(plan=plan,user=request.user).exists():
        # Create a new group and add the current user to it.
        Group.objects.create(plan=plan,user=request.user)

    # Redirect to a success page (or wherever you want).
    return redirect('plan')

@login_required
def group_delete(request, pk):
    plan = get_object_or_404(Plan, pk=pk)
    # Check if the user is already a member of the group.
    if Group.objects.filter(plan=plan,user=request.user).exists():
        # Create a new group and add the current user to it.
        group = get_object_or_404(Group, plan=plan, user=request.user)
        group.delete()

    # Redirect to a success page (or wherever you want).
    return redirect('plan')

@login_required
def plan_map(request,pk):
    plan = get_object_or_404(Plan, pk=pk)
    group = Group.objects.filter(plan=plan)

    # group에 속한 user들의 id 리스트 생성
    user_ids = group.values_list('user', flat=True)
    # UserLocation에서 해당 user들의 위치 정보 가져오기
    user_locations = UserLocation.objects.filter(user__in=user_ids)
    user_locations_json = serialize('json', user_locations)
    #user_locations_json2 = json.dumps(user_locations_json, ensure_ascii=False)
    return render(request, 'plan/plan_map.html', {'user_locations_json':user_locations_json})
