from django.conf import settings
from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import render_to_string, get_template


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
