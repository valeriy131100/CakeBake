import json
import threading
import time
import uuid

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_POST
from yookassa import Configuration, Payment

from .models import User

temped_orders = {}


def login_or_register(request):
    """Вход или создание регистрация нового пользователя."""
    # TODO: handle messages
    payload = {"redirect": "/"}

    if request.method == "POST":
        json_data = json.loads(request.body)
        email = json_data["email"]
        password = json_data["password"]

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            payload["message"] = "Вход выполнен."
        else:
            if User.objects.filter(username=email).exists():
                payload["message"] = "Пользователь с таким email уже зарегистрирован."
                return JsonResponse(payload)

            user = User.objects.create_user(username=email, email=email, password=password)
            login(request, user)
            # TODO: send email with creds
            payload["message"] = "Регистрация успешна, проверьте Вашу почту."

    return JsonResponse(payload)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def index(request):
    context = {}
    if request.user.is_authenticated:
        context['is_auth'] = True
        context['username'] = request.user.username

    return TemplateResponse(request, "index.html", context)


def profile(request):
    return render(request, "lk.html")


def check_payment_until_confirm(payment_id, subscription_uuid):
    while True:
        payment = Payment.find_one(payment_id)
        if payment.status == "canceled":
            temped_orders.pop(subscription_uuid)
            return
        if payment.status == "succeeded":
            order = temped_orders[subscription_uuid]
            # save order here

            print("Order finished!")
            print(order)

            return

        time.sleep(5)


@require_POST
def payment(request):
    order_description = json.loads(request.body)
    order_uuid = uuid.uuid4()

    Configuration.account_id = settings.YOOKASSA_ACCOUNT_ID
    Configuration.secret_key = settings.YOOKASSA_SECRET_KEY

    yoo_payment = Payment.create(
        {
            "amount": {"value": order_description["Cost"], "currency": "RUB"},
            "confirmation": {
                "type": "redirect",
                "return_url": request.build_absolute_uri(reverse(profile)),
            },
            "capture": True,
            "description": None,
        }
    )

    temped_orders[order_uuid] = order_description

    threading.Thread(
        target=check_payment_until_confirm,
        args=[yoo_payment.id, order_uuid],
        daemon=True,
    ).start()

    return JsonResponse(
        {"status": "success", "redirect": yoo_payment.confirmation.confirmation_url}
    )
