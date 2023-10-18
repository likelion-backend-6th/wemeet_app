from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils import timezone

from .forms import LoginForm, UserRegistrationForm
from .models import UserLocation
from plan.models import Plan, Group


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
    now_date = timezone.now()
    # 참여중 약속 수
    plan_ids = Group.objects.filter(user=request.user).values_list("plan_id", flat=True)

    plans = (
        Plan.objects.filter(id__in=plan_ids)
        .annotate(month=TruncMonth("time"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )

    # 지나간 약속
    past_plans = Plan.objects.filter(id__in=plan_ids, time__lt=now_date).order_by(
        "time"
    )

    # 다가오는 약속
    upcoming_plans = Plan.objects.filter(id__in=plan_ids, time__gt=now_date).order_by(
        "time"
    )

    return render(
        request,
        "accountapp/dashboard.html",
        {
            "section": "dashboard",
            "plans": plans,
            "past_plans": past_plans,
            "upcoming_plans": upcoming_plans,
            "now_date": now_date,
        },
    )


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


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data["email"]
            associated_users = get_user_model().objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "wemeet 비밀번호 재설정"
                    email_template_name = "registration/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        "domain": "127.0.0.1:8000",
                        "site_name": "wemeet",
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        "token": default_token_generator.make_token(user),
                        "protocol": "http",
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(
                            subject,
                            email,
                            "csy5501@gmail.com",
                            [user.email],
                            fail_silently=False,
                        )
                    except BadHeaderError:
                        return HttpResponse("Invalid header found.")
                    return redirect("/account/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(
        request=request,
        template_name="registration/password_reset.html",
        context={"password_reset_form": password_reset_form},
    )
