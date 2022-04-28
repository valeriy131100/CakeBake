from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe

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
    AdvertisingCompany, TotalAmount,
)


@admin.register(TotalAmount)
class TotalAmountAdmin(admin.ModelAdmin):
    list_display = ('name', 'count_total_amount')

    def count_total_amount(self, obj):
        all_advertising_companies = AdvertisingCompany.objects.all()
        total_amount = 0
        for advertising_company in all_advertising_companies:
            total_amount += advertising_company.total_amount
        return mark_safe(f'<h3>{total_amount}</h3>')


@admin.register(AdvertisingCompany)
class AdvertisingCompanyAdmin(admin.ModelAdmin):
    list_display = ('title', 'total_amount')


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
