from django.urls import path
from rest_framework.routers import SimpleRouter, DefaultRouter
from . import views

# router = DefaultRouter()
# router.register(r'', views.PlanViewSet, basename='plan'),
#
# urlpatterns =[
#     *router.urls,
# ]

urlpatterns = [
    # path('<uuid:pk>/',views.PlanViewSet.as_view({'get':'retrieve'}), name='plan_detail'),
    path("", views.PlanList.as_view(), name="plan"),
    path("create/", views.plan_create, name="plan_create"),
    path("check_password/", views.check_password, name="check_password"),
    path("<uuid:pk>/", views.PlanDetail.as_view(), name="plan_detail"),
    path("<uuid:pk>/edit", views.plan_edit, name="plan_edit"),
    path("<uuid:pk>/delete", views.plan_delete, name="plan_delete"),
    path("<uuid:pk>/group", views.group_create, name="group_create"),
    path("<uuid:pk>/group/delete", views.group_delete, name="group_delete"),
    path("<uuid:pk>/comment/create", views.comment_create, name="comment_create"),
    path("<uuid:pk>/map", views.plan_map, name="plan_map"),
    path("<uuid:pk>/mail", views.plan_mail, name="plan_mail"),
]
