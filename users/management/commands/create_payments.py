from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from materials.models import Course, Lesson
from users.models import Payment

User = get_user_model()


class Command(BaseCommand):
    help = 'Create test payments using ORM'

    def handle(self, *args, **options):

        user = User.objects.first()
        course = Course.objects.first()
        lesson = Lesson.objects.first()

        if not user:
            self.stdout.write(self.style.ERROR('No users found'))
            return

        Payment.objects.create(
            user=user,
            course=course,
            payment_amount=1000.00,
            payment_method=Payment.CASH
        )

        Payment.objects.create(
            user=user,
            lesson=lesson,
            payment_amount=500.00,
            payment_method=Payment.TRANSFER
        )

        self.stdout.write(self.style.SUCCESS('Payments successfully created'))
