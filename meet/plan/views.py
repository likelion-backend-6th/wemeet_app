import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import requests
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



    # model = Plan
    # form_class = PlanForm
    # template_name = 'plan/plan_form.html'
    # def form_valid(self, form):
    #     form.instance.owner = self.request.user
    #
    #     # Use the Kakao Maps Geocoding API to convert the address to latitude and longitude.
    #     response = requests.get('https://dapi.kakao.com/v2/local/search/address.json',
    #                             params={'query': form.instance.address}, headers={'Authorization': '717b45c4557cde712f061696cae0de82'})
    #     geodata = response.json()
    #
    #     if geodata['documents']:
    #         form.instance.latitude = float(geodata['documents'][0]['y'])
    #         form.instance.longitude = float(geodata['documents'][0]['x'])
    #     else:
    #         # Set default values or handle the error appropriately.
    #         form.instance.latitude = None
    #         form.instance.longitude = None
    #
    #     return super().form_valid(form)
    # def get_success_url(self):
    #     return reverse('plan')

class  PlanUpdate(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Plan
    form_class = PlanForm
    template_name = 'plan/plan_form.html'

    # 작성자만 수정 가능하도록
    def test_func(self):
        plan = self.get_object()
        if self.request.user == plan.owner:
            return True
        return False

    def get_success_url(self):
        return reverse('plan')

@login_required
def plan_delete(request,pk):
    plan = get_object_or_404(Plan, pk=pk)
    if plan.owner == request.user:
        plan.delete()
    else:
        return reverse('plan')

    return redirect('plan')

@login_required()
def group_create(request, pk):
    plan = get_object_or_404(Plan, pk=pk)
    # Check if the user is already a member of the group.
    if not Group.objects.filter(plan=plan,user=request.user).exists():
        # Create a new group and add the current user to it.
        Group.objects.create(plan=plan,user=request.user)

    # Redirect to a success page (or wherever you want).
    return redirect('plan')

@login_required()
def group_delete(request, pk):
    plan = get_object_or_404(Plan, pk=pk)
    # Check if the user is already a member of the group.
    if Group.objects.filter(plan=plan,user=request.user).exists():
        # Create a new group and add the current user to it.
        group = get_object_or_404(Group, plan=plan, user=request.user)
        group.delete()


    # Redirect to a success page (or wherever you want).
    return redirect('plan')