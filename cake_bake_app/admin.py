import csv
from datetime import date

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponse
from django.utils.safestring import mark_safe

from .models import (
    Berry,
    Cake,
    CakeForm,
    Decor,
    LevelsQuantity,
    Order,
    ActualOrderProxy,
    Topping,
    User,
    AdvertisingCompany, TotalAmount,
)


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        file_name = f'{meta}{date.today()}'

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(file_name)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


@admin.register(TotalAmount)
class TotalAmountAdmin(admin.ModelAdmin):
    list_display = ('name', 'count_total_amount')

    def count_total_amount(self, obj):
        all_advertising_companies = AdvertisingCompany.objects.all()
        total_amount = 0
        for advertising_company in all_advertising_companies:
            total_amount += advertising_company.amount()

        return mark_safe(f'<h3>{total_amount}</h3>')


@admin.register(AdvertisingCompany)
class AdvertisingCompanyAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount')


@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(ExportCsvMixin, admin.ModelAdmin):
    actions = ["export_as_csv"]

    list_display = (
        '__str__', 'user', 'status', 'delivery_address',
        'delivery_date', 'delivery_time',
    )


@admin.register(ActualOrderProxy)
class OrderActualAdmin(admin.ModelAdmin):

    list_display = (
        '__str__', 'first_name', 'phone_number', 'status', 'delivery_address',
        'delivery_date', 'delivery_time',
    )
    readonly_fields = ('phone_number', 'first_name')

    def get_queryset(self, request):
        statuses_for_show = (
            Order.WAIT, Order.IN_PROCESS, Order.IN_DELIVERY
        )
        qs = super().get_queryset(request)
        return qs.filter(status__in=statuses_for_show)

    def first_name(self, obj):
        return obj.user.first_name

    def phone_number(self, obj):
        return obj.user.phone_number

    phone_number.short_description = 'Телефон'
    first_name.short_description = 'Имя'


@admin.register(CakeForm)
class CakeFormAdmin(admin.ModelAdmin):
    list_display = ('name', 'price',)


@admin.register(LevelsQuantity)
class LevelsQuantityAdmin(admin.ModelAdmin):
    list_display = ('name', 'price',)


@admin.register(Topping)
class ToppingAdmin(admin.ModelAdmin):
    list_display = ('name', 'price',)


@admin.register(Berry)
class BerryAdmin(admin.ModelAdmin):
    list_display = ('name', 'price',)


@admin.register(Decor)
class DecorAdmin(admin.ModelAdmin):
    list_display = ('name', 'price',)


@admin.register(User)
class CustomUserAdmin(ExportCsvMixin, UserAdmin):
    actions = ["export_as_csv"]

    list_display = (
        'username', 'email', 'phone_number', 'first_name', 'is_staff',
    )
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )
