from django.contrib.auth.models import AbstractUser
from django.db import models

from config import settings
from materials.models import Course, Lesson


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name="Email", help_text="Enter email")
    phone = models.CharField(max_length=35, blank=True, null=True, verbose_name="Phone", help_text="Enter phone")
    city = models.CharField(max_length=65, blank=True, null=True, verbose_name="City", help_text="Enter city")
    avatar = models.ImageField(upload_to="users/avatars", blank=True, null=True, verbose_name="Avatar",
                               help_text="Upload avatar")

    USERNAME_FIELD = "email"  # авторизация
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email


class Payment(models.Model):

    CASH = 'cash'
    TRANSFER = 'transfer'
    CARD = 'card'

    PAYMENT_METHOD_CHOICES = ((CASH, 'Cash payment'), (TRANSFER, 'Bank transfer'), (CARD, 'Bank card'),)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                             verbose_name="Email of user who made the payment",
                             help_text="Enter user email", related_name='payments')
    #не User на случай, если модель пользователя изменится — платежи не сломаются - Best Practice
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Payment date")
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Course paid',
                               help_text="Enter course paid")  # История оплат должна сохраняться
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Lesson paid',
                               help_text="Enter lesson paid")
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Payment amount",
                                         help_text="Enter payment amount")
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES, verbose_name='Payment method',
                                      help_text="Choose payment method")
    stripe_product_id = models.CharField(null=True, blank=True, max_length=500, verbose_name='Stripe product ID')
    # храним IDs, чтобы можно было проверить статус потом м можно было связать платёж со Stripe
    stripe_price_id = models.CharField(null=True, blank=True, max_length=500, verbose_name='Stripe price ID')
    stripe_session_id = models.CharField(null=True, blank=True, max_length=500
                                         , verbose_name='Stripe session ID')
    payment_url = models.URLField(null=True, blank=True, verbose_name="Stripe payment URL")

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    def __str__(self):
        return f'{self.user} - {self.payment_amount}'
