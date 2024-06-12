from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from houses.models import Apartment, House, WaterMeter
from api.serializers import (ApartmentSerializer, HouseSerializer,
                             WaterMeterSerializer)
from api.tasks import calculation_rent


class ReadOrCreateViewSet(mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.ListModelMixin,
                          GenericViewSet):
    pass


class HouseViewSet(ReadOrCreateViewSet):
    """Вьюсет дома."""

    queryset = House.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = HouseSerializer


class ApartmentViewSet(ReadOrCreateViewSet):
    """Вьюсет квартиры."""

    queryset = Apartment.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = ApartmentSerializer


class WaterMeterViewSet(ReadOrCreateViewSet):
    """Вьюсет счетчика."""

    queryset = WaterMeter.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = WaterMeterSerializer


class RentView(APIView):
    """
    APIView  расчета квартплаты. Запись ее в БД.
    """

    def get(self, request, *args, **kwargs):
        calculation_rent.delay(self.kwargs.get('house_id'),
                               self.kwargs.get('month'))
        return Response({'message': 'Расчет квартплаты запущен!'})
