from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.conf import settings

from courses.models import Course, Lesson


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser должен иметь is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser должен иметь is_superuser=True")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )
    phone_number = models.CharField(
        max_length=35,
        null=True,
        blank=True,
        verbose_name="Номер телефона",
        help_text="Укажите номер телефона",
    )
    city = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Город",
        help_text="Укажите город",
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        null=True,
        blank=True,
        verbose_name="Аватар",
        help_text="Загрузите аватар",
    )

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


<<<<<<< task_5_Documentation_and_Security
class Payment(models.Model):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="stripe_payments",
        verbose_name="Пользователь",
        help_text="Укажите пользователя",
    )
    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.CASCADE,
        related_name="user_payments",
        verbose_name="Курс",
        help_text="Укажите курс",
=======
class Payments(models.Model):
    METHOD_CASH = "cash"
    METHOD_TRANSFER = "transfer"
    METHOD_CHOICES = (
        (METHOD_CASH, "Наличные"),
        (METHOD_TRANSFER, "Перевод на счет"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="Пользователь",
        help_text="Укажите пользователя",
    )
    date_payment = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата оплаты",
        help_text="Укажите дату оплаты",
    )
    course_paid = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments",
        verbose_name="Оплаченный курс",
        help_text="Выберите оплаченный курс",
    )
    lesson_paid = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments",
        verbose_name="Оплаченный урок",
        help_text="Выберите оплаченный урок",
>>>>>>> develop
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
<<<<<<< task_5_Documentation_and_Security
        verbose_name="Сумма платежа",
        help_text="Укажите сумму платежа",
    )
    stripe_product_id = models.CharField(max_length=255, blank=True)
    stripe_price_id = models.CharField(max_length=255, blank=True)
    stripe_session_id = models.CharField(max_length=255, blank=True)
    payment_link = models.URLField(max_length=1000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
=======
        verbose_name="Сумма оплаты",
        help_text="Укажите сумму оплаты",
    )
    method_payment = models.CharField(
        max_length=20,
        choices=METHOD_CHOICES,
        verbose_name="Способ оплаты",
        help_text="Выберите способ оплаты",
    )
>>>>>>> develop

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
<<<<<<< task_5_Documentation_and_Security
        ordering = ("-created_at",)
=======

    def __str__(self):
        return f"{self.user} - {self.amount}"
>>>>>>> develop
