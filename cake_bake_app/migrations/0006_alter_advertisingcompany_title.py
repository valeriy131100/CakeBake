# Generated by Django 4.0.4 on 2022-04-29 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cake_bake_app', '0005_alter_cake_title_alter_order_cake_alter_user_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisingcompany',
            name='title',
            field=models.CharField(max_length=256, unique=True, verbose_name='Название компании'),
        ),
    ]
