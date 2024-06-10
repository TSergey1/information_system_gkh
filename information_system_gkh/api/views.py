from datetime import date

from django.db.models import F, OuterRef, Subquery, Sum
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .serializers import (ApartmentSerializer, HouseSerializer,
                          RentSerializer, WaterMeterSerializer)
from houses.models import Apartment, House, WaterMeter


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
    """APIView  расчета квартплаты."""

    def get(self, request, *args, **kwargs):
        house_id = self.kwargs.get('house_id')
        month = self.kwargs.get('month')

        prev_month_readings = WaterMeter.objects.filter(
            date__month=(month - 1),
            date__year=date.today().year,
            apartment=OuterRef('pk'),
            tariff=OuterRef('water_meter__tariff')
        )

        qw_st = (
            Apartment.objects.filter(house=house_id)
            .prefetch_related('water_meter')
            .filter(
                water_meter__date__month=month,
                water_meter__date__year=date.today().year
            ).annotate(
                previous_value=Subquery(prev_month_readings.values('value')),
                cost=((F('water_meter__value') - F('previous_value'))
                      * F('water_meter__tariff'))
            ).values(
                'number',
                'area',
                'cost'
            )
        )
        print(qw_st)
        return Response({'message': 'Это был GET-запрос!'})
