import django_filters

from users.models import Payment


class PaymentFilter(django_filters.FilterSet):
    course = django_filters.NumberFilter(field_name='course')  # фильтрация по курсу
    lesson = django_filters.NumberFilter(field_name='lesson')  # фильтрация по уроку
    payment_method = django_filters.CharFilter(field_name='payment_method')  # фильтрация по способу оплаты

    class Meta:
        model = Payment
        fields = ['course', 'lesson', 'payment_method']
