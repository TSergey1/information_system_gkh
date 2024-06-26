# Generated by Django 4.0.6 on 2024-06-10 19:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0002_alter_watermeter_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='watermeter',
            options={'default_related_name': 'water_meter', 'ordering': ('tariff',), 'verbose_name': 'Счетчик воды', 'verbose_name_plural': 'Счетчики воды'},
        ),
        migrations.AlterField(
            model_name='watermeter',
            name='date',
            field=models.DateField(default=datetime.date(2024, 6, 10), verbose_name='Дата показаний'),
        ),
    ]
