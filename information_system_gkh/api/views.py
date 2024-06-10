from datetime import date

from django.db.models import F, OuterRef, Subquery
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
        # qw_st = Apartment.objects.filter(house=house_id).prefetch_related(
        #     'water_meter'
        # ).filter(water_meter__date__month__range=(month-1, month),
        #          water_meter__date__year=date.today().year).values(
        #              'number',
        #              'area',
        #              'water_meter__date',
        #              'water_meter__value',
        #              'water_meter__tariff__price',
        #              )
        prev_month_readings = WaterMeter.objects.filter(
            date__month=(month - 1),
            date__year=date.today().year,
            apartment__house=house_id
        ).values('value')

        qw_st = (
            Apartment.objects.filter(house=house_id)
            .prefetch_related("water_meter")
            .filter(
                water_meter__date__month=month,
                water_meter__date__year=date.today().year,
            ).annotate(
                total_cost=F("water_meter__value")
                * F("water_meter__tariff__price"),
                prev_month_reading=Subquery(prev_month_readings),
                diff=F("water_meter__value") - OuterRef("prev_month_reading"),
            )
            .values(
                "number",
                "area",
                "water_meter__value",
                "water_meter__tariff__price",
                "total_cost",
                "prev_month_reading",
                "diff",
            )
        )
        print(qw_st)
        # all_rent = []
        # for value in qw_st:
        #     apartment = ''
        #     if not apartment:
        #         apartment = value['number']
        #     rez = {
        #         'Квартира №': value['number'],
        #         'Квартира ': value['number']
        #     }
        #     all_rent.append(rez)


        # rez = {
        #     '111': '112',
        #     '111': '112'
        # }
        # return Response(rez, status=status.HTTP_200_OK)
        return Response({'message': 'Это был GET-запрос!'})
