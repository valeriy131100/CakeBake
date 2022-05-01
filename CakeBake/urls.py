from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path
from django.views.generic.base import RedirectView

from cake_bake_app import views

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'))),
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login_or_register),
    path('logout/', views.logout_view),
    path('profile/', views.profile, name='profile'),
    path('payment/', views.payment),
    path('user_data/', views.user_data),
]
