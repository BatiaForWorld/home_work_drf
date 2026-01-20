from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from users.models import User, Payments
from users.serializers import UserSerializer, UserRegistrationSerializer, LoginSerializer, PaymentSerializer


class UserProfileViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer


class PaymentViewSet(ModelViewSet):
	queryset = Payments.objects.all()
	serializer_class = PaymentSerializer
	filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
	filterset_fields = ["course_paid", "lesson_paid", "method_payment"]
	ordering_fields = ["date_payment"]
	ordering = ["-date_payment"]


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
