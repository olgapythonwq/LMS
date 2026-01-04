from django.urls import path
from rest_framework.routers import SimpleRouter

from materials.views import CourseViewSet, LessonListAPIView, LessonRetrieveAPIView, LessonCreateAPIView, \
    LessonDestroyAPIView, LessonUpdateAPIView, SubscriptionAPIView, SubscriptionListAPIView
from materials.apps import MaterialsConfig
from . import views

app_name = MaterialsConfig.name

router = SimpleRouter()
router.register("courses", CourseViewSet)

urlpatterns = [
    path("lessons/", LessonListAPIView.as_view(), name="lessons-list"),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lessons-retrieve"),
    path("lessons/create/", LessonCreateAPIView.as_view(), name="lessons-create"),
    path("lessons/<int:pk>/delete/", LessonDestroyAPIView.as_view(), name="lessons-delete"),
    path("lessons/<int:pk>/update/", LessonUpdateAPIView.as_view(), name="lessons-update"),
    path('subscriptions/', SubscriptionAPIView.as_view(), name='subscriptions'),
    path('success/', views.payment_success, name='payment_success'),
    path('cancel/', views.payment_cancel, name='payment_cancel'),
    path('subscriptions/list/', SubscriptionListAPIView.as_view(), name='subscriptions-list'),
]

urlpatterns += router.urls
