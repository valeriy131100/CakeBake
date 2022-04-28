from django.shortcuts import render

from cake_bake_app.models import Order


def index(request):
    user_orders = Order.objects.filter(user=request.user).prefetch_related('cake')
    context = {
        'order_quantity': user_orders.count()
    }
    return render(request, 'index.html', context)


def profile(request):
    return render(request, 'lk.html')


def order_list(request):
    user_orders = Order.objects.filter(user=request.user).prefetch_related('cake')
    context = {
        'user_orders': user_orders,
        'order_quantity': user_orders.count()
    }
    return render(request, 'lk-order.html', context)
