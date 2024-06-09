from datetime import date

from django.shortcuts import get_object_or_404
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


# class RentViewSet(viewsets.ModelViewSet):
#     """Вьюсет квартплаты."""
#     serializer_class = RentSerializer
#     permission_classes = (AllowAny, )

#     def get_queryset(self):
#         house_id = self.kwargs.get('house_id')
#         month = self.kwargs.get('month')

#         # return get_object_or_404(
#         #     Apartment,
#         #     house=house_id
#         # ).apartments.filter('water_meter__date__month'==month)

#         return Apartment.objects.filter(house=house_id).prefetch_related(
#             'water_meter'
#         ).filter(date__month=month, date__year=date.today().year)


class RentView(APIView):
    """APIView  расчета квартплаты."""

    def get(self, request, *args, **kwargs):
        house_id = self.kwargs.get('house_id')
        month = self.kwargs.get('month')
        qw_st = Apartment.objects.filter(house=house_id).prefetch_related(
            'water_meter'
        ).filter(water_meter__date__month=month,
                 water_meter__date__year=date.today().year).values(
                     'number',
                     'area',
                     'water_meter__value',
                     'water_meter__tariff__price',
                     )
        print(qw_st)
        # rezult_dict = {}
        # for value in qw_st:

        # rez = {
        #     '111': '112',
        #     '111': '112'
        # }
        # return Response(rez, status=status.HTTP_200_OK)
        return Response({'message': 'Это был GET-запрос!'})
