from datetime import date

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


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


class House(models.Model):
    """Модель дома."""
    address = models.CharField(max_length=255, unique=True,
                               verbose_name='Адрес дома',)
    tariff_property = models.ForeignKey(Tariff,
                                        on_delete=models.CASCADE,
                                        verbose_name='Тариф общего имущества')

    class Meta:
        ordering = ('address',)
        verbose_name = 'Дом'
        verbose_name_plural = 'Дома'

    def __str__(self):
        return self.address


class Apartment(models.Model):
    """Модель квартиры."""
    number = models.PositiveSmallIntegerField(
        verbose_name='Номер квартиры',
        validators=[MinValueValidator(1), MaxValueValidator(5000)]
    )
    area = models.DecimalField(max_digits=3,
                               decimal_places=1,
                               verbose_name='Площадь квартиры',)
    house = models.ForeignKey(House, on_delete=models.CASCADE)

    class Meta:
        ordering = ('number',)
        default_related_name = 'apartments'
        verbose_name = 'Квартира'
        verbose_name_plural = 'Квартиры'

        constraints = [
            models.UniqueConstraint(
                fields=['number', 'house'],
                name='unique_name_measurement_unit'
            )
        ]

    def __str__(self):
        return str(self.number)


class WaterMeter(models.Model):
    """Модель счетчика воды."""

    value = models.PositiveIntegerField(
        verbose_name='Показания счетчика',
        validators=[MinValueValidator(1), MaxValueValidator(99999)],
        help_text='Введите показания до запятой'
    )
    date = models.DateField(
        # auto_now_add=True,
        default=date.today(),
        verbose_name='Дата показаний',
    )
    tariff = models.ForeignKey(Tariff,
                               on_delete=models.CASCADE,
                               verbose_name='Тариф',)
    apartment = models.ForeignKey(
        'Apartment',
        on_delete=models.CASCADE,
        verbose_name='Квартира',
    )

    class Meta:
        ordering = ('tariff',)
        default_related_name = 'water_meter'
        verbose_name = 'Счетчик воды'
        verbose_name_plural = 'Счетчики воды'

    def __str__(self):
        return str(self.value)


class Rent(models.Model):
    """Модель квартплаты."""
    apartment = models.ForeignKey(
        'Apartment',
        on_delete=models.CASCADE,
        verbose_name='Квартира',
    )
    cost_water = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        verbose_name='Водоснабжение'
    )
    cost_property = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        verbose_name='Содержание общего имущества'
    )
    date = models.DateField(
        auto_now_add=True,
        verbose_name='Дата показаний',
    )

    class Meta:
        ordering = ('apartment',)
        verbose_name = 'Квартплата'
        verbose_name_plural = 'Квартплаты'

    def __str__(self):
        return str(self.apartment)
