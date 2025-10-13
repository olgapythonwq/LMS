from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=35, blank=True, null=True, verbose_name="Course name",
                            help_text="Enter course name")
    preview = models.ImageField(upload_to="materials/courses/previews", blank=True, null=True,
                                verbose_name="Course preview", help_text="Upload course preview")
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="Course description",
                                   help_text="Enter course description")
    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=35, blank=True, null=True, verbose_name="Lesson name",
                            help_text="Enter lesson name")
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, verbose_name="Course name",
                               help_text="Choose course")
    preview = models.ImageField(upload_to="materials/lessons/previews", blank=True, null=True,
                                verbose_name="Lesson preview", help_text="Upload lesson preview")
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="Lesson description",
                                   help_text="Enter lesson description")
    video_link = models.URLField(blank=True, null=True, verbose_name="Video link", help_text="Enter video link")

    class Meta:
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"

    def __str__(self):
        return self.name
