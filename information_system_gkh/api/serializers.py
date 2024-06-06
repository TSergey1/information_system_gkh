from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from houses.models import Apartment, House, WaterMeter


class WaterMetreSerializer(serializers.ModelSerializer):
    """Сериализатор квартиры."""
    # number = serializers.IntegerField(required=False)
    # value = serializers.IntegerField(required=False)
    # id = serializers.IntegerField()

    class Meta:
        model = WaterMeter
        fields = ('id',
                  'number',
                  'value',
                  'tariff',)
        extra_kwargs = {'number': {'required': False},
                        'value': {'required': False}}


class ApartmentSerializer(serializers.ModelSerializer):
    """Сериализатор квартиры."""
    water_meter = WaterMetreSerializer(many=True)
    house = PrimaryKeyRelatedField(
        queryset=House.objects.all()
    )

    class Meta:
        model = Apartment
        fields = ('number',
                  'area',
                  'water_meter',
                  'house',)

    # def create(self, validated_data):
    #     water_meters = validated_data.pop('water_meter')
    #     apartment = Apartment.objects.create(**validated_data)
    #     for water_meter in water_meters:
    #         WaterMeter.objects.create(**water_meter)
    #     return apartment

    def create(self, validated_data):
        water_meters = validated_data.pop('water_meter')
        w_t = []
        for water_meter in water_meters:
            WaterMeter.objects.create(**water_meter)
        w = WaterMeter.objects.create(**water_meter)
        w_t.append(w)
        apartment = Apartment.objects.create(water_meter=w_t, **validated_data)
        # WaterMeter.objects.create(**water_meter)
        return apartment


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
