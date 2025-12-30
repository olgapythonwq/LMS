from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Course
from materials.services import create_stripe_payment, get_stripe_session_status
from users.filters import PaymentFilter
from users.models import User, Payment
from users.permissions import IsSelf
from users.serializers import UserSerializer, PaymentSerializer, UserPrivateSerializer, UserPublicSerializer


@extend_schema_view(
    post=extend_schema(
        summary="Create user",
        description="Creates a new user. Available for everybody.",
        tags=["Users"],
        responses={201: UserSerializer},
    )
)
class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)  # позволяет неавторизованным пользователям зарегистрироваться


@extend_schema_view(
    list=extend_schema(
        summary="Get list of users",
        description="Returns list of all users. Accessible for all users.",
        tags=["Users"],
    ),
    retrieve=extend_schema(
        summary="Get user details",
        description="Returns detailed information about a user. Accessible for all users.",
        tags=["Users"],
    ),
    create=extend_schema(
        summary="Create user",
        description="Creates a new user. Accessible for all users.",
        tags=["Users"],
    ),
    update=extend_schema(
        summary="Update user",
        description="Updates user data. Accessible for owners.",
        tags=["Users"],
    ),
    partial_update=extend_schema(
        summary="Partial update of user",
        description="Partially updates user data (PATCH). Accessible for owners.",
        tags=["Users"],
    ),
    destroy=extend_schema(
        summary="Delete user",
        description="Deletes a user. Accessible for owners.",
        tags=["Users"],
    ),
)
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


@extend_schema_view(
    get=extend_schema(
        summary="Get list of payments",
        description="Returns filtered and ordered list of payments.",
        tags=["Payments"],
        responses={200: PaymentSerializer(many=True)},
    )
)
class PaymentListAPIView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PaymentFilter

    ordering_fields = ['payment_date']
    ordering = ['payment_date']  # по умолчанию


@extend_schema_view(
    post=extend_schema(
        summary="Create payment",
        description="Creates Stripe payment session and returns payment URL.",
        tags=["Payments"],
        request={"application/json": {"type": "object",
                                      "properties": {"course_id": {"type": "integer"},},
                                      "required": ["course_id"],
                                      }
                 },
        responses={200: {"type": "object",
                         "properties": {"payment_url": {"type": "string"},}
                         }
                   },
    )
)
class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        course = get_object_or_404(Course, id=request.data["course_id"])

        # Фиксируем сумму платежа
        payment = Payment.objects.create(
            user=request.user,
            course=course,
            payment_amount=course.price,  # Фиксируем текущую цену из курса в платёж
            payment_method=Payment.CARD,
        )

        stripe_data = create_stripe_payment(payment)  # передаём Payment в Stripe

        # сохраняем Stripe-данные
        payment.stripe_product_id = stripe_data["product_id"]
        payment.stripe_price_id = stripe_data["price_id"]
        payment.stripe_session_id = stripe_data["session_id"]
        payment.payment_url = stripe_data["payment_url"]
        payment.save()

        return Response({"payment_url": payment.payment_url}, status=201)


class PaymentStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Check payment status",
        description="Returns Stripe payment status for a given payment_id",
        tags=["Payments"],
        responses={200: dict}
    )
    def get(self, request, payment_id):
        payment = get_object_or_404(Payment, id=payment_id, user=request.user)
        if not payment.stripe_session_id:
            return Response({"error": "Stripe session not found"}, status=404)

        session_data = get_stripe_session_status(payment.stripe_session_id)
        return Response(session_data)
