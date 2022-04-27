# Generated by Django 4.0.4 on 2022-04-27 07:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cake_bake_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Berry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Название')),
                ('price', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Цена')),
            ],
            options={
                'verbose_name': 'Ягоды',
                'verbose_name_plural': 'Ягоды',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Cake',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, verbose_name='Название')),
                ('text', models.CharField(blank=True, max_length=50, verbose_name='Надпись')),
                ('price', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Цена')),
                ('berry', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cakes', to='cake_bake_app.berry', verbose_name='Ягоды')),
            ],
            options={
                'verbose_name': 'Торт',
                'verbose_name_plural': 'Торты',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='CakeForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Название')),
                ('price', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Цена')),
            ],
            options={
                'verbose_name': 'Форма',
                'verbose_name_plural': 'Формы',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Decor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Название')),
                ('price', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Цена')),
            ],
            options={
                'verbose_name': 'Декор',
                'verbose_name_plural': 'Виды декора',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='LevelsQuantity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Название')),
                ('price', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Цена')),
            ],
            options={
                'verbose_name': 'Количество уровней',
                'verbose_name_plural': 'Количество уровней',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, verbose_name='Комментарий к заказу')),
                ('delivery_address', models.TextField(verbose_name='Адрес доставки')),
                ('delivery_date', models.DateField(verbose_name='Дата доставки')),
                ('delivery_time', models.TimeField(verbose_name='Время доставки')),
                ('delivery_comment', models.TextField(blank=True, verbose_name='Комментарий для курьера')),
                ('price', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Общая стоимость')),
                ('created_at', models.DateTimeField(verbose_name='Дата и время создания')),
                ('status', models.CharField(choices=[('WAIT', 'Ожидает обработки'), ('IN_PROCESS', 'В обработке'), ('IN_DELIVERY', 'В доставке'), ('DONE', 'Выполнен')], default='WAIT', max_length=11, verbose_name='Статус')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='Topping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Название')),
                ('price', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Цена')),
            ],
            options={
                'verbose_name': 'Топпинг',
                'verbose_name_plural': 'Топпинги',
                'ordering': ('name',),
            },
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('first_name',), 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=10, verbose_name='Имя'),
        ),
        migrations.CreateModel(
            name='OrderCake',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cake', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cake_bake_app.cake')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cake_bake_app.order')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='cakes',
            field=models.ManyToManyField(related_name='orders', through='cake_bake_app.OrderCake', to='cake_bake_app.cake', verbose_name='Список тортов'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='Клиент'),
        ),
        migrations.AddField(
            model_name='cake',
            name='decor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cakes', to='cake_bake_app.decor', verbose_name='Декор'),
        ),
        migrations.AddField(
            model_name='cake',
            name='form',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cakes', to='cake_bake_app.cakeform', verbose_name='Форма'),
        ),
        migrations.AddField(
            model_name='cake',
            name='levels',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cakes', to='cake_bake_app.levelsquantity', verbose_name='Количество уровней'),
        ),
        migrations.AddField(
            model_name='cake',
            name='topping',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cakes', to='cake_bake_app.topping', verbose_name='Топпинг'),
        ),
    ]
