from django.db import models

from config import settings


class Course(models.Model):
    name = models.CharField(max_length=35, blank=True, null=True, verbose_name="Course name",
                            help_text="Enter course name")
    preview = models.ImageField(upload_to="materials/courses/previews", blank=True, null=True,
                                verbose_name="Course preview", help_text="Upload course preview")
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="Course description",
                                   help_text="Enter course description")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name="Course owner", help_text="Enter the owner of the course",
                              related_name="courses")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Course price")
    last_notification = models.DateTimeField(null=True, blank=True, verbose_name="Last update notification time")

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self):
        return self.name or "Unnamed course"


class Lesson(models.Model):
    name = models.CharField(max_length=35, blank=True, null=True, verbose_name="Lesson name",
                            help_text="Enter lesson name")
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, verbose_name="Course name",
                               help_text="Choose course", related_name='lessons')
    preview = models.ImageField(upload_to="materials/lessons/previews", blank=True, null=True,
                                verbose_name="Lesson preview", help_text="Upload lesson preview")
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="Lesson description",
                                   help_text="Enter lesson description")
    video_link = models.URLField(blank=True, null=True, verbose_name="Video link", help_text="Enter video link")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name="Lesson owner", help_text="Enter the owner of the lesson",
                              related_name='lessons')

    class Meta:
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"

    def __str__(self):
        return self.name or "Unnamed lesson"


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Subscriber",
                             related_name="subscriptions")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Course name",
                               related_name='subscriptions')

    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"
        unique_together = ('user', 'course')

    def __str__(self):
        return f'{self.user} subscribed for {self.course}'
