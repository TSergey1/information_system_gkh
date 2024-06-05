from django.core.validators import MaxValueValidator
from django.db import models


DICT_ERRORS = {
   'value_max': 'Показания должны содержать не более 5 символов'
}

TYPE_WATER = [
        ('hot', 'Горячая'),
        ('cold', 'Холодная'),
    ]


class Tariff(models.Model):
    """Модель тарифа."""
    NAME_TARIFF = [
        ('hot', 'Горячая вода'),
        ('cold', 'Холодная вода'),
        ('property', 'Содержание общего имущества')
    ]
    name = models.CharField('Название', choices=NAME_TARIFF,
                            unique=True, max_length=50)
    price = models.DecimalField(max_digits=5,
                                decimal_places=2,
                                verbose_name='Цена',)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'

    def __str__(self):
        return self.name


class ValueWaterMeter(models.Model):
    """Модель показания счетчика."""
    value = models.PositiveIntegerField(
        verbose_name='Показания счетчика',
        validators=[
            MaxValueValidator(5, message='{0}'.format(
                DICT_ERRORS.get('value_max')))
        ],
        help_text='Введите показания до запятой'
    )
    date = models.DateField(
        auto_now_add=True,
        verbose_name='Дата и время показаний',
    )

    class Meta:
        ordering = ('date',)
        verbose_name = 'Паказание счетчика'
        verbose_name_plural = 'Паказания счетчика'

    def __str__(self):
        return self.value


class WaterMeter(models.Model):
    """Модель счетчика воды."""

    number = models.CharField(
        blank=True,
        null=True,
        max_length=50,
        verbose_name='Номер прибора'
    )
    value = models.ForeignKey(
        ValueWaterMeter,
        on_delete=models.CASCADE,
        blank=True,
        verbose_name='Показания счетчика',
    )
    tariff = models.ForeignKey(Tariff,
                               on_delete=models.CASCADE,
                               verbose_name='Тариф',)

    class Meta:
        ordering = ('value__date',)
        default_related_name = 'water_meter'
        verbose_name = 'Счетчик воды'
        verbose_name_plural = 'Счетчики воды'

    def __str__(self):
        return self.value


class Apartment(models.Model):
    """Модель квартиры."""
    number = models.PositiveSmallIntegerField(verbose_name='Номер квартиры')
    area = models.FloatField(verbose_name='Площадь квартиры')
    water_meter = models.ForeignKey(
        WaterMeter,
        on_delete=models.CASCADE,
        verbose_name='Cчетчик воды',
        blank=True,
    )
    house = models.ForeignKey('House', on_delete=models.CASCADE)

    class Meta:
        ordering = ('number',)
        default_related_name = 'apartments'
        verbose_name = 'Квартира'
        verbose_name_plural = 'Квартиры'

    def __str__(self):
        return self.number


class House(models.Model):
    """Модель дома."""
    address = models.CharField(max_length=255, verbose_name='Адрес дома',)

    class Meta:
        ordering = ('address',)
        verbose_name = 'Дом'
        verbose_name_plural = 'Дома'

    def __str__(self):
        return self.address
