# Generated by Django 4.0.4 on 2022-05-02 05:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cake_bake_app', '0010_remove_order_email_remove_order_name_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='totalamount',
            options={'verbose_name': 'Сумма всех заказов', 'verbose_name_plural': 'Суммарные стоимости заказов'},
        ),
    ]