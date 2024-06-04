from django.contrib import admin

from .models import Apartment, House, Tariff, WaterMeter


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'price',
        'date'
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(WaterMeter)
class WaterMeterAdmin(admin.ModelAdmin):
    list_display = (
        'number',
        'value',
        'type_water'
    )
    search_fields = ('number',)
    list_filter = ('number',)
    empty_value_display = '-пусто-'


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = (
        'namber',
        'area',
    )
    empty_value_display = '-пусто-'


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = (
        'address',
        'apartment',
    )
    search_fields = ('address', )
    list_filter = ('author', 'score')
    empty_value_display = '-пусто-'
