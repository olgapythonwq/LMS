from datetime import timedelta

import stripe
from django.conf import settings
from django.utils import timezone
from materials.tasks import send_course_update_email


stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(course):
    return stripe.Product.create(
        name=course.name,
        description=course.description,
    )


def create_stripe_price(product_id, amount):
    return stripe.Price.create(
        product=product_id,
        unit_amount=int(amount * 100),  # копейки!
        currency="usd",
    )


def create_stripe_session(price_id):
    return stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price": price_id,
            "quantity": 1,
        }],
        mode="payment",
        success_url=settings.STRIPE_SUCCESS_URL,
        cancel_url=settings.STRIPE_CANCEL_URL,
    )


def create_stripe_payment(payment):
    product = stripe.Product.create(name=payment.course.name)
    price = stripe.Price.create(
        product=product.id,
        unit_amount=int(payment.payment_amount * 100),
        currency="usd",
    )
    session = stripe.checkout.Session.create(
        line_items=[{"price": price.id,"quantity": 1,}],
        mode="payment",
        success_url="http://localhost:8000/materials/success/",
        cancel_url="http://localhost:8000/materials/cancel/",
    )
    return {
        "product_id": product.id,
        "price_id": price.id,
        "session_id": session.id,
        "payment_url": session.url,
    }


def get_stripe_session_status(session_id: str) -> dict:
    """Получает данные сессии оплаты из Stripe по session_id."""
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        return {
            "id": session.id,
            "payment_status": session.payment_status,  # 'paid', 'unpaid', 'no_payment_required'
            "amount_total": session.amount_total,
            "currency": session.currency,
            "customer_email": session.customer_email,
            "payment_intent": session.payment_intent,
        }
    except stripe.error.StripeError as e:
        # логируем ошибку, можно вернуть пустой dict или raise
        return {"error": str(e)}


def notify_course_if_needed(course):
    """Отправляет уведомление об обновлении курса, если прошло более 4 часов с последней рассылки."""
    now = timezone.now()

    if not course.last_notification or now - course.last_notification >= timedelta(minutes=10):
        send_course_update_email.delay(course.id)
        course.last_notification = now
        course.save(update_fields=['last_notification'])
