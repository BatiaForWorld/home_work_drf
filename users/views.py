from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, ListModelMixin, DestroyModelMixin
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.permissions import IsOwner
from users.serializers import UserSerializer, UserPublicSerializer, UserRegistrationSerializer, LoginSerializer


class UserProfileViewSet(RetrieveModelMixin, UpdateModelMixin, ListModelMixin, DestroyModelMixin, GenericViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer

	def get_permissions(self):
		if self.action in {"list", "retrieve"}:
			self.permission_classes = [IsAuthenticated]
		elif self.action in {"update", "partial_update", "destroy"}:
			self.permission_classes = [IsAuthenticated, IsOwner]
		return [permission() for permission in self.permission_classes]

	def get_serializer_class(self):
		if self.action == "list":
			return UserPublicSerializer
		if self.action == "retrieve":
			obj = self.get_object()
			if self.request.user == obj:
				return UserSerializer
			return UserPublicSerializer
		return UserSerializer


class UserRegistrationAPIView(APIView):
	permission_classes = []

	def post(self, request, *args, **kwargs):
		serializer = UserRegistrationSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()
		refresh = RefreshToken.for_user(user)
		return Response(
			{"refresh": str(refresh), "access": str(refresh.access_token)},
			status=status.HTTP_201_CREATED,
		)


class LoginAPIView(APIView):
	permission_classes = []

	def post(self, request, *args, **kwargs):
		serializer = LoginSerializer(data=request.data, context={"request": request})
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data["user"]
		refresh = RefreshToken.for_user(user)
		return Response({"refresh": str(refresh), "access": str(refresh.access_token)})


class LogoutAPIView(APIView):
	permission_classes = [IsAuthenticated]

	def post(self, request, *args, **kwargs):
		return Response(status=status.HTTP_204_NO_CONTENT)
