from django.db import models


class Tariff(models.Model):
    """Модель тарифа."""
    name = models.CharField('Название', max_length=255)
    price = models.DecimalField(max_digits=5,
                                decimal_places=2,
                                verbose_name='Цена',)
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время изменения тарифа',
    )

    class Meta:
        ordering = ('date',)
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'

    def __str__(self):
        return self.price


class ValueWaterMeter(models.Model):
    """Модель показания счетчика."""
    value = models.PositiveIntegerField(
        verbose_name='Показания счетчика',
        max_length=5,
        help_text='Введите показания до запятой'
    )
    date = models.DateTimeField(
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

    TYPE_WATER = [
        ('hot', 'Горячая'),
        ('cold', 'Холодная'),
    ]
    number = models.CharField(
        unique=True,
        blank=True,
        verbose_name='Номер прибора'
    )
    value = models.ForeignKey(
        ValueWaterMeter,
        on_delete=models.CASCADE,
        verbose_name='Показания счетчика',
    )
    type_water = models.CharField(
        choices=TYPE_WATER,
        default='cold',
        verbose_name='Тип воды'
    )

    tariff = models.ManyToManyField(Tariff,
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
    namber = models.PositiveSmallIntegerField(unique=True,
                                              verbose_name='Номер квартиры')
    area = models.FloatField(verbose_name='Площадь квартиры')
    water_meter = models.ForeignKey(
        WaterMeter,
        on_delete=models.CASCADE,
        verbose_name='Cчетчик воды',
    )

    class Meta:
        ordering = ('namber',)
        default_related_name = 'apartment'
        verbose_name = 'Квартира'
        verbose_name_plural = 'Квартиры'

    def __str__(self):
        return self.namber


class House(models.Model):
    """Модель дома."""

    apartment = models.ForeignKey(
        Apartment,
        on_delete=models.CASCADE,
        verbose_name='Квартира',
    )
    address = models.CharField(max_length=255, verbose_name='Адрес дома',)

    class Meta:
        ordering = ('address',)
        default_related_name = 'houses'
        verbose_name = 'Дом'
        verbose_name_plural = 'Дома'

    def __str__(self):
        return self.address
