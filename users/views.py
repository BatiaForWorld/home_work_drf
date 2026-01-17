from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin

from users.models import User
from users.serializers import UserSerializer, UserRegistrationSerializer, LoginSerializer


class UserProfileViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer


class UserRegistrationAPIView(APIView):
	def post(self, request, *args, **kwargs):
		serializer = UserRegistrationSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()
		token, _ = Token.objects.get_or_create(user=user)
		return Response({"token": token.key}, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
	def post(self, request, *args, **kwargs):
		serializer = LoginSerializer(data=request.data, context={"request": request})
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data["user"]
		token, _ = Token.objects.get_or_create(user=user)
		return Response({"token": token.key})


class LogoutAPIView(APIView):
	def post(self, request, *args, **kwargs):
		token = Token.objects.filter(user=request.user).first()
		if token:
			token.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
