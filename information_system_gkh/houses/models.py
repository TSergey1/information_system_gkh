from django.core.validators import MaxValueValidator
from django.db import models


DICT_ERRORS = {
   'value_max': 'Показания должны содержать не более 5 символов'
}


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

    class Meta:
        ordering = ('address',)
        verbose_name = 'Дом'
        verbose_name_plural = 'Дома'

    def __str__(self):
        return self.address


class Apartment(models.Model):
    """Модель квартиры."""
    number = models.PositiveSmallIntegerField(verbose_name='Номер квартиры')
    area = models.FloatField(verbose_name='Площадь квартиры')
    house = models.ForeignKey(House, on_delete=models.CASCADE)

    class Meta:
        ordering = ('number',)
        default_related_name = 'apartments'
        verbose_name = 'Квартира'
        verbose_name_plural = 'Квартиры'

    def __str__(self):
        return str(self.number)


class WaterMeter(models.Model):
    """Модель счетчика воды."""

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
    tariff = models.ForeignKey(Tariff,
                               on_delete=models.CASCADE,
                               verbose_name='Тариф',)
    apartment = models.ForeignKey(
        'Apartment',
        on_delete=models.CASCADE,
        verbose_name='Квартира',
    )

    class Meta:
        ordering = ('date',)
        default_related_name = 'water_meter'
        verbose_name = 'Счетчик воды'
        verbose_name_plural = 'Счетчики воды'

    def __str__(self):
        return str(self.value)
