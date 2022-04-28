from django.shortcuts import render

from .models import LevelsQuantity, CakeForm, Topping, Berry, Decor, Order


temped_orders = {}


def prepare_components_list(query_set):
    query_set = query_set.order_by('id')

    list_ = ['Без'] + [component.name for component in query_set]

    costs = [0] + [
        int(component.price) for component in query_set
    ]

    return {
        'list': list_,
        'costs': costs
    }


def index(request):
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
        'order_quantity': user_orders.count()
    }

    user_orders = Order.objects.filter(user=request.user).prefetch_related('cake')
    order_quantity = {
        'order_quantity': user_orders.count()
    }

    return render(
        request, 'index.html',
        context={
            'components': components,
            'order_quantity': order_quantity,
            }
        )


def profile(request):
    return render(request, 'lk.html')


def order_list(request):
    user_orders = Order.objects.filter(user=request.user).prefetch_related('cake')
    context = {
        'user_orders': user_orders,
        'order_quantity': user_orders.count()
    }
    return render(request, 'lk-order.html', context)
