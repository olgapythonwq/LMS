from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from materials.models import Subscription


@shared_task
def send_course_update_email(course_id):
    subscriptions = Subscription.objects.filter(course_id=course_id).select_related('user', 'course')

    for sub in subscriptions:
        send_mail(
            subject=f'Course updated: {sub.course.name}',
            message='New materials have been added or updated in the course.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[sub.user.email],
            fail_silently=False,
        )
