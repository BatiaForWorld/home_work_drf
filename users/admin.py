from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from users.models import Payment, User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
	model = User
	list_display = ("id", "email", "first_name", "last_name", "is_staff", "is_active")
	list_filter = ("is_staff", "is_superuser", "is_active", "groups")
	search_fields = ("email", "first_name", "last_name")
	ordering = ("email",)

	fieldsets = (
		(None, {"fields": ("email", "password")}),
		("Персональные данные", {"fields": ("first_name", "last_name", "phone_number", "city", "avatar")}),
		("Права", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
		("Важные даты", {"fields": ("last_login", "date_joined")}),
	)

	add_fieldsets = (
		(
			None,
			{
				"classes": ("wide",),
				"fields": ("email", "password1", "password2", "is_staff", "is_superuser"),
			},
		),
	)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
	list_display = ("id", "user", "course", "amount", "created_at")
	search_fields = ("stripe_session_id", "stripe_product_id", "stripe_price_id")
