import json
import threading
import time
import uuid

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST
from rest_framework import serializers
from yookassa import Configuration, Payment

from .models import User, Cake, CakeComponent, AdvertisingCompany

from .models import LevelsQuantity, CakeForm, Topping, Berry, Decor, Order

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
            payload["message"] = "Вход выполнен"
        else:
            if User.objects.filter(username=email).exists():
                payload["message"] = "Неверный пароль"
                return JsonResponse(payload)

            user = User.objects.create_user(username=email, email=email, password=password)
            login(request, user)
            # TODO: send email with creds
            payload["message"] = "Регистрация успешна"

    return JsonResponse(payload)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def prepare_components_list(query_set):
    query_set = query_set.order_by('id')

    list_ = ['Без'] + [component.name for component in query_set]

    costs = [0.0] + [
        float(component.price) for component in query_set
    ]

    pks = [None] + [component.id for component in query_set]

    return {
        'list': list_,
        'costs': costs,
        'pks': pks
    }


def index(request):
    ad_parameter = request.GET.get('ad_company')
    if ad_parameter:
        now = timezone.now()
        try:
            advertising_company = AdvertisingCompany.objects.get(
                key_word=ad_parameter,
                start_date__lt=now,
                end_date__gt=now
            )
        except AdvertisingCompany.DoesNotExist:
            advertising_company = None
    else:
        advertising_company = None

    levels = LevelsQuantity.objects.all()
    forms = CakeForm.objects.all()
    toppings = Topping.objects.all()
    berries = Berry.objects.all()
    decors = Decor.objects.all()

    components = {
        'levels': prepare_components_list(levels),
        'forms': prepare_components_list(forms),
        'toppings': prepare_components_list(toppings),
        'berries': prepare_components_list(berries),
        'decors': prepare_components_list(decors),
    }

    context = {
        'components': components,
        'advertising_company': advertising_company.id
    }
    if request.user.is_authenticated:
        context['is_auth'] = True
        context['username'] = request.user.username

    return render(request, 'index.html', context)


def profile(request):
    return render(request, 'lk.html')


def check_payment_until_confirm(payment_id, subscription_uuid):
    while True:
        payment = Payment.find_one(payment_id)
        if payment.status == "canceled":
            temped_orders.pop(subscription_uuid)
            return
        if payment.status == "succeeded":
            cake, order = temped_orders[subscription_uuid]
            cake.save()
            order.save()
            return

        time.sleep(5)


class CakeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cake
        fields = (
            'levels',
            'form',
            'topping',
            'berry',
            'decor',
            'text'
        )


class OrderSerializer(serializers.ModelSerializer):
    cake = CakeSerializer()

    class Meta:
        model = Order
        fields = (
            'cake',
            'comment',
            'delivery_address',
            'delivery_date',
            'delivery_time',
            'delivery_comment',
            'advertising_company'
        )


@require_POST
def payment(request):
    if request.user.is_anonymous:
        return JsonResponse({'user': 'Unauthorised'}, status=401)

    unvalidated_order = json.loads(request.body)

    serializer = OrderSerializer(data=unvalidated_order)
    serializer.is_valid(raise_exception=True)

    order_description = serializer.validated_data

    cost = 0

    for field, field_value in order_description['cake'].items():
        if isinstance(field_value, CakeComponent):
            cost += field_value.price

        if (field == 'text') and field_value:
            cost += 500

    cake = Cake(
        title='Торт на заказ',
        price=cost,
        **order_description['cake']
    )

    order_description['cake'] = cake

    order = Order(
        user=request.user,
        price=cost,
        created_at=timezone.now(),
        **order_description
    )

    order_uuid = uuid.uuid4()

    Configuration.account_id = settings.YOOKASSA_ACCOUNT_ID
    Configuration.secret_key = settings.YOOKASSA_SECRET_KEY

    yoo_payment = Payment.create({
        "amount": {
            "value": cost,
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": request.build_absolute_uri(reverse(profile))
        },
        "capture": True,
        "description": None
    })

    temped_orders[order_uuid] = [cake, order]

    threading.Thread(
        target=check_payment_until_confirm,
        args=[yoo_payment.id, order_uuid],
        daemon=True
    ).start()

    return JsonResponse(
        {
            'status': 'success',
            'redirect': yoo_payment.confirmation.confirmation_url
        }
    )


def order_list(request):
    user_orders = Order.objects.filter(user=request.user).prefetch_related('cake')
    context = {
        'user_orders': user_orders,
        'order_quantity': user_orders.count()
    }
    return render(request, 'lk-order.html', context)
