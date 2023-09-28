from django.urls import path
from rest_framework.routers import SimpleRouter,DefaultRouter
from . import views
router = DefaultRouter()
router.register(r'', views.PlanViewSet, basename='plan'),

urlpatterns =[
    *router.urls,
]

urlpatterns += [
   path('<uuid:pk>/',views.PlanViewSet.as_view({'get':'retrieve'}), name='plan_detail'),
]