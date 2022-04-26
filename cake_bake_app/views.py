from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def profile(request):
    return render(request, 'lk.html')


def profile_order(request):
    return render(request, 'lk-order.html')
