from django.urls import path
from rest_framework.routers import SimpleRouter

from users.apps import UsersConfig
from users.views import UserProfileViewSet, UserRegistrationAPIView, LoginAPIView, LogoutAPIView

app_name = UsersConfig.name

router = SimpleRouter()
router.register("profile", UserProfileViewSet, basename="profile")

urlpatterns = [
	path("register/", UserRegistrationAPIView.as_view(), name="register"),
	path("login/", LoginAPIView.as_view(), name="login"),
	path("logout/", LogoutAPIView.as_view(), name="logout"),
]

urlpatterns += router.urls
