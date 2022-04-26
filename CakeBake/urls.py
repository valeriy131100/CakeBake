from django.contrib import admin
from django.urls import path

from cake_bake_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('profile', views.profile),
    path('profile/order', views.profile_order)
]
