# Generated by Django 4.0.4 on 2022-04-29 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cake_bake_app', '0006_alter_advertisingcompany_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisingcompany',
            name='clicks',
            field=models.IntegerField(default=0, verbose_name='Число кликов'),
        ),
    ]