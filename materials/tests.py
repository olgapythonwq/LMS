from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="user2@mail.ru")
        self.course = Course.objects.create(name="Maths")
        self.lesson = Lesson.objects.create(name="Algebra", course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("materials:lessons-retrieve", args=(self.lesson.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.lesson.name)

    def test_lesson_update(self):
        url = reverse("materials:lessons-update", args=(self.lesson.id,))
        data = {'name': "Stats"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Stats")

    def test_lesson_create(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:lessons-create")  # POST обычно на list endpoint
        data = {"name": "Geometry", "course": self.course.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_lessons_list(self):
        url = reverse("materials:lessons-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)  # с пагинацией

    def test_lesson_delete(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:lessons-delete", args=(self.lesson.id,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="user2@mail.ru")
        self.course = Course.objects.create(name="Maths")
        self.client.force_authenticate(user=self.user)

    def test_add_subscription(self):
        url = reverse("materials:subscriptions")
        data = {"course_id": self.course.id}

        # До подписки - нет объектов
        self.assertEqual(Subscription.objects.count(), 0)

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Subscription added")
        self.assertEqual(Subscription.objects.count(), 1)  # подписка создана

    def test_remove_subscription(self):
        # Сначала создаём подписку вручную
        Subscription.objects.create(user=self.user, course=self.course)
        self.assertEqual(Subscription.objects.count(), 1)

        url = reverse("materials:subscriptions")
        data = {"course_id": self.course.id}

        response = self.client.post(url, data)  # POST повторно → удаление
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Subscription deleted")
        self.assertEqual(Subscription.objects.count(), 0)  # подписка удалена

    def test_subscription_unauthenticated(self):
        self.client.force_authenticate(user=None)
        url = reverse("materials:subscriptions")
        data = {"course_id": self.course.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="user2@mail.ru")
        self.course = Course.objects.create(name="Maths")
        self.client.force_authenticate(user=self.user)

    def test_course_update(self):
        url = reverse("materials:course-detail", args=(self.course.id,))
        data = {'name': "History"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "History")
