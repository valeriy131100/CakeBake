from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    Berry,
    Cake,
    CakeForm,
    OrderCake,
    Decor,
    LevelsQuantity,
    Order,
    Topping,
    User,
)


@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderCake)
class OrderCakeAdmin(admin.ModelAdmin):
    pass


@admin.register(CakeForm)
class CakeFormAdmin(admin.ModelAdmin):
    pass


@admin.register(LevelsQuantity)
class LevelsQuantityAdmin(admin.ModelAdmin):
    pass


@admin.register(Topping)
class ToppingAdmin(admin.ModelAdmin):
    pass


@admin.register(Berry)
class BerryAdmin(admin.ModelAdmin):
    pass


@admin.register(Decor)
class DecorAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)
