from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def deactivate_inactive_users():
    threshold = timezone.now() - timedelta(days=30)

    users = User.objects.filter(last_login__lt=threshold, is_active=True)

    users.update(is_active=False)
