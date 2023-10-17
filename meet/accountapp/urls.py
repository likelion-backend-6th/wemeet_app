from django.contrib.auth.forms import SetPasswordForm
from django.urls import path, include, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = "accountapp"

urlpatterns = [
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/common/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/common/password_reset_confirm.html",
            success_url=reverse_lazy("accountapp:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/common/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("password_reset/", views.password_reset_request, name="password_reset"),
    path("", include("django.contrib.auth.urls")),
    # path("login/",LoginView.as_view(),name='login'),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("register/", views.register, name="register"),
    path("logged_out/", views.logged_out, name="logged_out"),
    path("update_location/", views.update_location, name="update_location"),
]
