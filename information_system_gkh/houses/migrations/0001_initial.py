# Generated by Django 4.0.6 on 2024-06-09 12:52

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Apartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5000)], verbose_name='Номер квартиры')),
                ('area', models.FloatField(verbose_name='Площадь квартиры')),
            ],
            options={
                'verbose_name': 'Квартира',
                'verbose_name_plural': 'Квартиры',
                'ordering': ('number',),
                'default_related_name': 'apartments',
            },
        ),
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255, unique=True, verbose_name='Адрес дома')),
            ],
            options={
                'verbose_name': 'Дом',
                'verbose_name_plural': 'Дома',
                'ordering': ('address',),
            },
        ),
        migrations.CreateModel(
            name='Tariff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('hot', 'Горячая вода'), ('cold', 'Холодная вода'), ('property', 'Содержание общего имущества')], max_length=50, unique=True, verbose_name='Название')),
                ('price', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Цена')),
            ],
            options={
                'verbose_name': 'Тариф',
                'verbose_name_plural': 'Тарифы',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='WaterMeter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.PositiveIntegerField(help_text='Введите показания до запятой', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(99999)], verbose_name='Показания счетчика')),
                ('date', models.DateField(auto_now_add=True, verbose_name='Дата показаний')),
                ('apartment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='houses.apartment', verbose_name='Квартира')),
                ('tariff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='houses.tariff', verbose_name='Тариф')),
            ],
            options={
                'verbose_name': 'Счетчик воды',
                'verbose_name_plural': 'Счетчики воды',
                'ordering': ('date',),
                'default_related_name': 'water_meter',
            },
        ),
        migrations.AddField(
            model_name='apartment',
            name='house',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='houses.house'),
        ),
        migrations.AddConstraint(
            model_name='apartment',
            constraint=models.UniqueConstraint(fields=('number', 'house'), name='unique_name_measurement_unit'),
        ),
    ]
