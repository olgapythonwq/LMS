from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import (
    PaymentCreateAPIView,
    PaymentListAPIView,
    PaymentStatusAPIView,
    UserCreateAPIView,
    UserViewSet,
)

app_name = UsersConfig.name

router = SimpleRouter()
router.register('', UserViewSet)

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('payments/', PaymentListAPIView.as_view(), name='payments-list'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('payments/create/', PaymentCreateAPIView.as_view(), name='payment-create'),
    path('payments/<int:payment_id>/status/', PaymentStatusAPIView.as_view(), name='payment_status'),
]

urlpatterns += router.urls
