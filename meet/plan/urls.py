from django.urls import path
from rest_framework.routers import SimpleRouter,DefaultRouter
from . import views
router = DefaultRouter()
router.register(r'v', views.PlanViewSet, basename='plan1'),
router.register(r'v2', views.PlanViewSet2, basename='plan2')
urlpatterns =[
    *router.urls,
]

# urlpatterns += [
#     path('',views.PlanList.as_view(), name='plan3'),
#     path('api/', views.PlanListAPI.as_view(), name='plan4'),
# ]