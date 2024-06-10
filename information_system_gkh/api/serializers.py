from datetime import date

from rest_framework import serializers

from houses.models import Apartment, House, WaterMeter

DICT_ERRORS = {
    'unique_number': 'Квартира с таким номером уже создана ранее.',
    'invalid_number': ('Веден неверный номер квартиры.'
        'Значение дожно быть от 1 до 5000'),
    'invalid_value': ('Значение дожно быть от 1 до 99999')
}


class WaterMeterSerializer(serializers.ModelSerializer):
    """Сериализатор счетчика."""
    class Meta:
        model = WaterMeter
        fields = ('id',
                  'value',
                  'date',
                  'tariff',
                  'apartment', )

    def validate_value(self, value):
        if value <= 0 or value > 99999:
            raise serializers.ValidationError(
                '{0}'.format(DICT_ERRORS.get('invalid_value'))
            )
        return value

    def create(self, validated_data):
        """
        Повторное отправление данных в текущем месяце обновит данные в БД.
        """

        value = validated_data.pop('value')

        if WaterMeter.objects.filter(
            date__month=date.today().month,
            date__year=date.today().year,
            **validated_data
        ).exists():

            water_meter = WaterMeter.objects.filter(
                **validated_data
            )[0]
            water_meter.value = value
            water_meter.save()
        else:
            water_meter = WaterMeter.objects.create(
                value=value,
                **validated_data)
        return water_meter


class ApartmentSerializer(serializers.ModelSerializer):
    """Сериализатор квартиры."""
    water_meter = WaterMeterSerializer(many=True, read_only=True)

    class Meta:
        model = Apartment
        fields = ('water_meter',
                  'number',
                  'area',
                  'house',)
        read_only_fields = ('water_meter',)
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Apartment.objects.all(),
                fields=['number', 'house'],
                message='{0}'.format(DICT_ERRORS.get('unique_number'))
            )
        ]

    def validate_number(self, value):
        if value <= 0 or value > 5000:
            raise serializers.ValidationError(
                '{0}'.format(DICT_ERRORS.get('invalid_number'))
            )
        return value


class HouseSerializer(serializers.ModelSerializer):
    """Сериализатор дома."""
    apartments = serializers.SerializerMethodField()

    class Meta:
        model = House
        fields = ('apartments',
                  'address',
                  'tariff_property', )

    def get_apartments(self, obj):
        """Получение квартир."""
        return obj.apartments.values('id', 'number', 'area', 'house')


class RentSerializer(serializers.Serializer):
    """Сериализатор квартплаты."""
    class Meta:
        model = House
        fields = ('id', 'text', 'author', 'image', 'group', 'pub_date')
