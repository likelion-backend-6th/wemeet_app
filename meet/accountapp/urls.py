from django.contrib.auth.views import LoginView
from django.urls import path, include
from . import views

app_name = "accountapp"

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    # path("login/",LoginView.as_view(),name='login'),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("register/", views.register, name="register"),
    path("logged_out/", views.logged_out, name="logged_out"),
    path("update_location/", views.update_location, name="update_location"),
]
