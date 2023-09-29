from django.urls import path
from rest_framework.routers import SimpleRouter,DefaultRouter
from . import views
#router = DefaultRouter()
# router.register(r'', views.PlanViewSet, basename='plan'),
#
# urlpatterns =[
#     *router.urls,
# ]

urlpatterns = [
  # path('<uuid:pk>/',views.PlanViewSet.as_view({'get':'retrieve'}), name='plan_detail'),
    path('', views.PlanList.as_view(), name='plan'),
    path('create/', views.PlanCreate.as_view(),name='plan_create'),
    path('<uuid:pk>/', views.PlanDetail.as_view(), name='plan_detail'),
    path('<uuid:pk>/edit',  views.PlanUpdate.as_view(),name='plan_edit'),
    path('<uuid:pk>/delete', views.plan_delete, name='plan_delete' ),

]