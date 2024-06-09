from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from .serializers import (ApartmentSerializer, HouseSerializer,
                          WaterMeterSerializer)
from houses.models import Apartment, House, WaterMeter


class ReadOrCreateViewSet(mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.ListModelMixin,
                          GenericViewSet):
    pass


class HouseViewSet(ReadOrCreateViewSet):
    """Вьюсет дома."""

    queryset = House.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = HouseSerializer


class ApartmentViewSet(ReadOrCreateViewSet):
    """Вьюсет квартиры."""

    queryset = Apartment.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ApartmentSerializer


class WaterMeterViewSet(ReadOrCreateViewSet):
    """Вьюсет счетчика."""

    queryset = WaterMeter.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = WaterMeterSerializer
