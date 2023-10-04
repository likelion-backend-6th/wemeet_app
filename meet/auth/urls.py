from rest_framework_nested import routers
from .viewsets import RefreshViewSet, LoginViewSet, RegisterViewSet
from accountapp.viewsets import UserViewSet

router = routers.SimpleRouter()
router.register(r"user", UserViewSet, basename="user")
router.register(r"register", RegisterViewSet, basename="auth-register")
router.register(r"login", LoginViewSet, basename="auth-login")
router.register(r"refresh", RefreshViewSet, basename="auth-refresh")

urlpatterns = [
    *router.urls,
]
