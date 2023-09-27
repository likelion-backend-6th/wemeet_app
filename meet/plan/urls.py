from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views
# router = SimpleRouter()
# router.register(r'', views.PlanList.as_view(), basename='plan-list')

# urlpatterns =[
#     *router.urls,
# ]

urlpatterns = [
    path('',views.PlanList.as_view(), name='plan'),
]