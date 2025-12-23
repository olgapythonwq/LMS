from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.filters import PaymentFilter
from users.models import User, Payment
from users.permissions import IsSelf
from users.serializers import UserSerializer, PaymentSerializer, UserPrivateSerializer, UserPublicSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)  # позволяет неавторизованным пользователям зарегистрироваться


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        # создание пользователя
        if self.action == "create":
            return UserSerializer
        # просмотр профиля
        if self.action == 'retrieve':
            user = self.get_object()
            if self.request.user == user:
                return UserPrivateSerializer
            return UserPublicSerializer
        # обновление пользователя
        if self.action in ["update", "partial_update"]:
            return UserPrivateSerializer
        return UserPublicSerializer

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsSelf()]
        return [IsAuthenticated()]


class PaymentListAPIView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PaymentFilter

    ordering_fields = ['payment_date']
    ordering = ['payment_date']  # по умолчанию
