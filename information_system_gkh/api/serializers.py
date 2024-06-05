from rest_framework import serializers

from houses.models import Apartment, House, WaterMeter


class WaterMetreSerializer(serializers.ModelSerializer):
    """Сериализатор квартиры."""
    class Meta:
        model = WaterMeter
        fields = ('namber',
                  'value',
                  'type_water',
                  'tariff',)


class ApartmentSerializer(serializers.ModelSerializer):
    """Сериализатор квартиры."""
    class Meta:
        model = Apartment
        fields = ('id',
                  'namber',
                  'area',
                  'water_meter',)


class HouseSerializer(serializers.ModelSerializer):
    """Сериализатор дома."""
    apartment = ApartmentSerializer(many=True)

    class Meta:
        model = House
        fields = ('apartment',
                  'address',)
