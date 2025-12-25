from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson, Subscription
from materials.validators import validate_video_link


class CourseSerializer(ModelSerializer):
    is_subscribed = SerializerMethodField()

    def get_is_subscribed(self, course):
        user = self.context['request'].user
        if user.is_anonymous:
            return False

        return Subscription.objects.filter(user=user, course=course).exists()

    class Meta:
        model = Course
        fields = "__all__"

class LessonSerializer(ModelSerializer):
    video_link = serializers.URLField(required=False, allow_null=True,validators=[validate_video_link])

    class Meta:
        model = Lesson
        fields = "__all__"

class CourseDetailSerializer(ModelSerializer):
    count_lessons = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_count_lessons(self, course):
        return Lesson.objects.filter(course=course).count()  #БД возвращает количество

    class Meta:
        model = Course
        fields = ('name', 'preview', 'description', 'count_lessons', 'lessons')
