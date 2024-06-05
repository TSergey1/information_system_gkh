from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from houses.models import Apartment, House, WaterMeter


class WaterMetreSerializer(serializers.ModelSerializer):
    """Сериализатор квартиры."""
    # number = serializers.IntegerField(required=None)

    class Meta:
        model = WaterMeter
        fields = ('number',
                  'value',
                  'tariff',)
        extra_kwargs = {'number': {'required': False}}


class ApartmentSerializer(serializers.ModelSerializer):
    """Сериализатор квартиры."""
    water_meter = WaterMetreSerializer(many=True)
    # house = PrimaryKeyRelatedField(
    #     queryset=House.objects.all()
    # )

    class Meta:
        model = Apartment
        fields = ('number',
                  'area',
                  'water_meter',
                  'house',)


class HouseSerializer(serializers.ModelSerializer):
    """Сериализатор дома."""
    apartments = serializers.SerializerMethodField()

    class Meta:
        model = House
        fields = ('apartments',
                  'address',)

    def get_apartments(self, obj):
        """Получение квартир."""
        return obj.apartments.values('id',
                                     'area')
