import json
import threading
import time
import uuid

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from rest_framework import serializers
from yookassa import Configuration, Payment

from .models import User, Cake, CakeComponent, AdvertisingCompany

from .models import LevelsQuantity, CakeForm, Topping, Berry, Decor, Order
from .utils.mail import send_creds_mail


temped_orders = {}


def login_or_register(request):
    """Вход или создание регистрация нового пользователя."""

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

            # в случае если пользователя с таким email нет - создаем
            user = User.objects.create_user(username=email, email=email, password=password)
            login(request, user)
            send_creds_mail(
                recipient_name="",
                recipient_mail=email,
                password=password,
            )
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
            advertising_company.clicks += 1
            advertising_company.save()
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
        'advertising_company': (advertising_company.id if advertising_company
                                else None)
    }
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        context['is_auth'] = True
        context['username'] = request.user.username
        # for order
        context['user_first_name'] = user.first_name
        context['user_phone_number'] = str(user.phone_number)
        context['user_email'] = user.email
        context['user_orders_count'] = user.orders.count()
    return render(request, 'index.html', context)


@login_required()
def user_data(request):
    # TODO: костыль для запросов из фронтенда
    # TODO: использовать везде в js коде для работы с данными юзера
    context = {'message': 'error'}

    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        try:
            latest_order = Order.objects.filter(
                user__username=request.user
            ).latest('created_at')
        except Order.DoesNotExist:
            latest_order = None

        context['is_auth'] = True
        context['username'] = request.user.username
        # for order
        context['user_first_name'] = user.first_name
        context['user_phone_number'] = (
            str(user.phone_number) if user.phone_number else ''
        )
        context['user_email'] = user.email
        if latest_order is not None:
            context['user_address'] = latest_order.delivery_address
        context['message'] = 'ok'

    return JsonResponse(context)


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

    unvalidated_order = json.loads(request.body)

    serializer = OrderSerializer(data=unvalidated_order)
    serializer.is_valid(raise_exception=True)

    order_description = serializer.validated_data

    if request.user.is_anonymous:
        password = User.objects.make_random_password(10)
        # TODO: add checking if user already exist on frontend
        user = User.objects.create_user(
            first_name=unvalidated_order['name'],
            username=unvalidated_order['email'],
            email=unvalidated_order['email'],
            phone_number=unvalidated_order['phone_number'],
            password=password,
        )
        # TODO: add exception processing
        send_creds_mail(
            recipient_name=user.first_name,
            recipient_mail=user.email,
            password=password
        )
        del password

    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)

    cost = 0

    for field, field_value in order_description['cake'].items():
        if isinstance(field_value, CakeComponent):
            cost += field_value.price

        if (field == 'text') and field_value:
            cost += 500

    cake = Cake(
        title=f'Торт на заказ ({user.email})',
        price=cost,
        **order_description['cake']
    )

    order_description['cake'] = cake

    order = Order(
        user=user,
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


@login_required()
def profile(request):
    """Вью личного кабинета клиента со списком заказов."""
    # TODO: merge with user_data

    try:
       user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        # TODO: add logging
        return redirect('index')

    context = {
        'is_auth': True,
        'username': request.user.username,
        'user_first_name': user.first_name,
        'user_phone': str(user.phone_number),
        'user_email': user.email,
        'user_orders_count': user.orders.count(),
    }

    if request.method == 'POST':
        data = json.loads(request.body)

        if data['action'] == 'load':
            return JsonResponse(context)

        if data['action'] == 'edit_user':
            user = User.objects.get(username=request.user.username)
            user.email = data['user_email']
            user.username = data['user_email']
            user.phone_number = data['user_phone']
            user.first_name = data['user_first_name']
            user.save()
            return JsonResponse({'message': 'success'})

    # if GET
    # TODO: load orders in js with ajax
    user_orders = Order.objects.filter(user=request.user).prefetch_related('cake')
    context['user_orders'] = user_orders
    context['order_quantity'] = user_orders.count()

    return render(request, 'lk.html', context)
