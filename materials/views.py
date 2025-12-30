from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson, Subscription
from materials.paginators import MyPagination
from materials.serializers import CourseSerializer, LessonSerializer, CourseDetailSerializer, \
    SubscriptionResponseSerializer
from users.permissions import IsModerator, IsNotModerator, IsOwner
from django.shortcuts import render


@extend_schema_view(
    list=extend_schema(
        summary="Get list of courses",
        description="Returns list of all courses. Accessible for all users.",
        tags=["Courses"],
    ),
    retrieve=extend_schema(
        summary="Get course details",
        description="Returns detailed information about a course. "
                    "Access depends on user permissions.",
        tags=["Courses"],
    ),
    create=extend_schema(
        summary="Create course",
        description="Creates a new course. Available only for non-moderators.",
        tags=["Courses"],
    ),
    update=extend_schema(
        summary="Update course",
        description="Updates course data. Available for moderators or owners.",
        tags=["Courses"],
    ),
    partial_update=extend_schema(
        summary="Partial update of course",
        description="Partially updates course data (PATCH). Available for moderators or owners.",
        tags=["Courses"],
    ),
    destroy=extend_schema(
        summary="Delete course",
        description="Deletes a course. Available for owner.",
        tags=["Courses"],
    ),
)
class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    pagination_class = MyPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAuthenticated, IsNotModerator]
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action == "destroy":
            self.permission_classes = [IsAuthenticated, IsNotModerator | IsOwner]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]


@extend_schema_view(
    post=extend_schema(
        summary="Create lesson",
        description="Creates a new lesson. Available only for non-moderators.",
        tags=["Lessons"],
    )
)
class LessonCreateAPIView(CreateAPIView):
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()

    permission_classes = [IsAuthenticated, IsNotModerator]


@extend_schema_view(
    get=extend_schema(
        summary="Get list of lessons",
        description="Returns list of all lessons. Accessible for all users.",
        tags=["Lessons"],
    ),
)
class LessonListAPIView(ListAPIView):
    pagination_class = MyPagination
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


@extend_schema_view(
    get=extend_schema(
        summary="Get lesson details",
        description="Returns detailed information about a lesson. "
                    "Access depends on user permissions.",
        tags=["Lessons"],
    ),
)
class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


@extend_schema_view(
    put=extend_schema(
        summary="Update lesson",
        description="Updates lesson data. Available for moderators or owners.",
        tags=["Lessons"],
    ),
    patch=extend_schema(
        summary="Partial update of lesson",
        description="Partially updates lesson data. Available for moderators or owners.",
        tags=["Lessons"],
    ),
)
class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


@extend_schema_view(
    delete=extend_schema(
        summary="Delete lesson",
        description="Deletes a lesson. Available for owner.",
        tags=["Lessons"],
    ),
)
class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()

    permission_classes = [IsAuthenticated, IsNotModerator | IsOwner]


class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Subscribe / unsubscribe to course",
        description="Creates or deletes a subscription to a course.",
        tags=["Subscriptions"],
        request={"application/json": {"type": "object","properties": {"course_id": {"type": "integer"},},
                                      "required": ["course_id"],
                                      },
                 },
        responses={200: SubscriptionResponseSerializer},
    )
    def post(self, request):
        user = request.user  # Получаем пользователя
        course_id = request.data.get('course_id')  # Получаем id курса из запроса
        course = get_object_or_404(Course, id=course_id)  # Получаем объект курса или 404
        subscription = Subscription.objects.filter(user=user, course=course)  # Ищем подписку

        # Если подписка есть — удаляем
        if subscription.exists():
            subscription.delete()
            message = 'Subscription deleted'
        # Если подписки нет — создаём
        else:
            Subscription.objects.create(user=user, course=course)
            message = 'Subscription added'

        # Возвращаем ответ в API
        return Response({"message": message})


def payment_success(request):
    return render(request, "materials/success.html")

def payment_cancel(request):
    return render(request, "materials/cancel.html")
