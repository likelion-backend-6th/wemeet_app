from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone

from .forms import LoginForm, UserRegistrationForm
from .models import UserLocation
from plan.models import Plan,Group


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()

            new_user.backend = "django.contrib.auth.backends.ModelBackend"
            login(request, new_user)
            return redirect("plan")

    else:
        user_form = UserRegistrationForm()
    return render(request, "accountapp/register.html", {"user_form": user_form})


@login_required
def logged_out(request):
    logout(request)
    return redirect("accountapp:dashboard")


@login_required
def dashboard(request):
    now_date = timezone.now().date()
    # 참여중 약속 수
    plan_ids = Group.objects.filter(user=request.user).values_list(
        "plan_id", flat=True
    )

    plans = Plan.objects.filter(id__in=plan_ids)\
        .annotate(month=TruncMonth('time'))\
        .values('month')\
        .annotate(count=Count('id'))\
        .order_by('month')

    # 지나간 약속
    past_plans = Plan.objects.filter(id__in=plan_ids, time__lt=now_date).order_by('time')

    return render(request, "accountapp/dashboard.html", {"section": "dashboard",
                                                         "plans":plans,
                                                         "past_plans":past_plans})



def update_location(request):
    if request.method == "POST":
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")

        # 현재 로그인한 유저의 인스턴스 가져오기 (로그인 상태 가정)
        user = request.user

        # 새로운 UserLocation 인스턴스 생성하기
        user_location = UserLocation(user=user, latitude=latitude, longitude=longitude)
        user_location.save()

    return JsonResponse({"status": "success"}, safe=False)
