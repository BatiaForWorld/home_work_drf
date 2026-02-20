from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import Course
from users.models import Payment, User


class PaymentTestCase(APITestCase):
	"""Тесты API платежей пользователя."""

	def setUp(self):
		self.user = User.objects.create_user(email="payer@test.com", password="pass")
		self.course = Course.objects.create(
			title="Paid course",
			description="Course description",
			owner=self.user,
			price=1000,
		)

	@patch("users.views.create_stripe_session")
	@patch("users.views.create_stripe_price")
	@patch("users.views.create_stripe_product")
	def test_create_payment(self, create_product_mock, create_price_mock, create_session_mock):
		"""Создает платеж и возвращает ссылку Stripe Checkout."""
		self.client.force_authenticate(user=self.user)

		create_product_mock.return_value = {"id": "prod_test", "name": "Paid course"}
		create_price_mock.return_value = {"id": "price_test", "currency": "rub", "unit_amount": 100000}
		create_session_mock.return_value = {"id": "cs_test", "url": "https://checkout.stripe.com/test"}

		url = reverse("users:payment_create")
		response = self.client.post(url, data={"course": self.course.id})

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response.data["stripe_product_id"], "prod_test")
		self.assertEqual(response.data["stripe_price_id"], "price_test")
		self.assertEqual(response.data["stripe_session_id"], "cs_test")
		self.assertEqual(response.data["payment_link"], "https://checkout.stripe.com/test")
		self.assertEqual(Payment.objects.count(), 1)

	def test_create_payment_with_zero_price(self):
		"""Не позволяет создать платеж для бесплатного курса."""
		self.client.force_authenticate(user=self.user)
		self.course.price = 0
		self.course.save(update_fields=["price"])

		url = reverse("users:payment_create")
		response = self.client.post(url, data={"course": self.course.id})

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertIn("course", response.data)
