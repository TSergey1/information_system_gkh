from django.contrib import admin

from .models import (Apartment, House, Tariff, WaterMeter)


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'price',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(WaterMeter)
class WaterMeterAdmin(admin.ModelAdmin):
    list_display = (
        'value',
        'date',
        'apartment',
        'tariff',
    )
    search_fields = ('apartment',)
    list_filter = ('apartment',)
    empty_value_display = '-пусто-'


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = (
        'number',
        'area',
        'house',
    )
    empty_value_display = '-пусто-'


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = (
        'address',
    )
    search_fields = ('address', )
    empty_value_display = '-пусто-'
