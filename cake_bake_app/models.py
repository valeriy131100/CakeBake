from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    """Кастомный пользователь."""

    email = models.EmailField(_("email address"), unique=True)
    phone_number = PhoneNumberField(
        verbose_name=_('Phone'),
        blank=True, null=True,
        unique=True,
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("first_name",)

    def __str__(self):
        return self.email


class AdvertisingCompany(models.Model):
    title = models.CharField(
        verbose_name="Название компании",
        max_length=256,
        unique=True,
    )
    key_word = models.CharField(
        verbose_name="Ключевое слово",
        max_length=256,
    )
    start_date = models.DateTimeField(
        verbose_name="Дата начала",
    )
    end_date = models.DateTimeField(
        verbose_name="Дата окончания",
    )
    readonly_fields = ('amount',)

    clicks = models.IntegerField(
        verbose_name='Число кликов',
        default=0
    )

    @admin.display(description='Сумма')
    def amount(self):
        orders = self.orders.all()
        company_amount = 0
        for order in orders:
            company_amount += order.price

        return company_amount

    class Meta:
        verbose_name = "Рекламная компания"
        verbose_name_plural = "Рекламные компании"
        ordering = ("title",)

    def __str__(self):
        return self.title


class TotalAmount(models.Model):
    name = models.CharField(
        verbose_name="Название",
        max_length=20,
    )

    class Meta:
        verbose_name = "Сумма всех заказов"
        verbose_name_plural = 'Суммарные стоимости заказов'

    def __str__(self):
        return self.name


class Order(models.Model):
    """Заказ."""

    WAIT = "WAIT"
    IN_PROCESS = "IN_PROCESS"
    IN_DELIVERY = "IN_DELIVERY"
    DONE = "DONE"
    STATUSES = (
        (WAIT, "Ожидает обработки"),
        (IN_PROCESS, "В обработке"),
        (IN_DELIVERY, "В доставке"),
        (DONE, "Выполнен"),
    )

    user = models.ForeignKey(
        to="User",
        verbose_name="Клиент",
        related_name="orders",
        on_delete=models.CASCADE,
    )
    cake = models.ForeignKey(
        to="Cake",
        verbose_name="Торт",
        related_name="orders",
        on_delete=models.CASCADE,
        null=True,
    )

    comment = models.TextField(
        verbose_name="Комментарий к заказу",
        blank=True,
    )

    delivery_address = models.TextField(
        verbose_name="Адрес доставки",
    )
    delivery_date = models.DateField(verbose_name="Дата доставки")
    delivery_time = models.TimeField(verbose_name="Время доставки")
    delivery_comment = models.TextField(
        verbose_name="Комментарий для курьера",
        blank=True,
    )

    price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        verbose_name="Общая стоимость",
    )

    created_at = models.DateTimeField(
        verbose_name="Дата и время создания",
    )
    status = models.CharField(
        verbose_name="Статус",
        max_length=11,
        choices=STATUSES,
        default=WAIT,
    )
    advertising_company = models.ForeignKey(
        to="AdvertisingCompany",
        verbose_name="Рекламная компания",
        on_delete=models.CASCADE,
        related_name="orders",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ("created_at",)

    def __str__(self):
        return self.cake.title


class ActualOrderProxy(Order):
    """Для удобного отображения необработанных заказов."""

    class Meta:
        proxy = True
        verbose_name = "Заказ"
        verbose_name_plural = "Необработанные заказы"
        ordering = ("created_at",)

    def __str__(self):
        return self.cake.title


class Cake(models.Model):
    """Модель как для тортов собираемых пользователем,
    так и для готовых типовых тортов."""

    title = models.CharField(
        verbose_name="Название",
        max_length=200,
        blank=True,
    )
    levels = models.ForeignKey(
        to="LevelsQuantity",
        verbose_name="Количество уровней",
        on_delete=models.CASCADE,
        related_name="cakes",
    )
    form = models.ForeignKey(
        to="CakeForm",
        verbose_name="Форма",
        on_delete=models.CASCADE,
        related_name="cakes",
    )

    topping = models.ForeignKey(
        to="Topping",
        verbose_name="Топпинг",
        on_delete=models.CASCADE,
        related_name="cakes",
    )
    berry = models.ForeignKey(
        to="Berry",
        verbose_name="Ягоды",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="cakes",
    )
    decor = models.ForeignKey(
        to="Decor",
        verbose_name="Декор",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="cakes",
    )
    text = models.CharField(
        verbose_name="Надпись",
        max_length=50,
        blank=True,
    )

    price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        verbose_name="Цена",
    )

    class Meta:
        verbose_name = "Торт"
        verbose_name_plural = "Торты"
        ordering = ("title",)

    def __str__(self):
        return self.title


class CakeComponent(models.Model):
    """Абстрактный класс компонента торта."""

    name = models.CharField(
        verbose_name="Название",
        max_length=20,
        unique=True
    )
    price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        verbose_name="Цена",
    )

    class Meta:
        abstract = True


class LevelsQuantity(CakeComponent):
    """Справочник уровней торта."""

    class Meta:
        verbose_name = "Количество уровней"
        verbose_name_plural = "Количество уровней"
        ordering = ("name",)

    def __str__(self):
        return self.name


class CakeForm(CakeComponent):
    """Справочник форм тортов."""

    class Meta:
        verbose_name = "Форма"
        verbose_name_plural = "Формы"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Topping(CakeComponent):
    """Справочник топпингов."""

    class Meta:
        verbose_name = "Топпинг"
        verbose_name_plural = "Топпинги"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Berry(CakeComponent):
    """Справочник ягод."""

    class Meta:
        verbose_name = "Ягоды"
        verbose_name_plural = "Ягоды"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Decor(CakeComponent):
    """Справочник декора."""

    class Meta:
        verbose_name = "Декор"
        verbose_name_plural = "Виды декора"
        ordering = ("name",)

    def __str__(self):
        return self.name
