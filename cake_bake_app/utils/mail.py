from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import get_template

from cake_bake_app.models import Order


def send_creds_mail(recipient_name='', recipient_mail='', password=''):
    """Отсылка письма с паролем на адрес нового пользователя."""

    context = {
        'user': recipient_name,
        'email': recipient_mail,
        'password': password,
    }
    message = get_template('mail.html').render(context)
    email_message = EmailMessage(
        'Регистрация на сайте CakeBake',
        message,
        settings.EMAIL_HOST_USER,
        [recipient_mail, ],
    )
    email_message.content_subtype = 'html'

    return email_message.send()


def send_order_mail(recipient_name='', recipient_mail='', order=None, cake=None):
    """Отсылка письма с информацией о заказе на адрес пользователя."""

    order_statuses = dict(Order.STATUSES)

    context = {
        'user_name': recipient_name,

        'created_at': order.created_at,
        'order_number': '12345TEST',  # TODO: add order unique number
        'price': order.price,
        'status': order_statuses[order.status],

        'delivery_address': order.delivery_address,
        'delivery_date': order.delivery_date,
        'delivery_time': order.delivery_time,
        'delivery_comment': order.delivery_comment,

        'cake_comment': order.comment,
        'cake_levels': cake.levels,
        'cake_form': cake.form,
        'cake_topping': cake.topping,
        'cake_berry': cake.berry,
        'cake_decor': cake.decor,
        'cake_text': cake.text,
    }

    message = get_template('order_mail.html').render(context)
    email_message = EmailMessage(
        'Ваш заказ на сайте CakeBake принят',
        message,
        settings.EMAIL_HOST_USER,
        [recipient_mail, ],
    )
    email_message.content_subtype = 'html'

    return email_message.send()
