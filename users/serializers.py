from django.contrib.auth import authenticate
from rest_framework import serializers

from users.models import User, Payments


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    payments = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "city",
            "avatar",
            "payments",
        )
        read_only_fields = ("id", "email")

    def get_payments(self, obj):
        request = self.context.get("request")
        user = request.user if request and request.user.is_authenticated else obj
        queryset = Payments.objects.filter(user=user)
        return PaymentSerializer(queryset, many=True).data


class UserRegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "phone_number",
            "city",
            "avatar",
        )

    def validate(self, attrs):
        if attrs.get("password1") != attrs.get("password2"):
            raise serializers.ValidationError("Пароли не совпадают")
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password1")
        validated_data.pop("password2", None)
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(
            request=self.context.get("request"),
            email=attrs.get("email"),
            password=attrs.get("password"),
        )
        if not user:
            raise serializers.ValidationError("Неверный email или пароль")
        attrs["user"] = user
        return attrs
