from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .serializers import ApartmentSerializer, HouseSerializer
from houses.models import Apartment, House


class HouseViewSet(viewsets.ModelViewSet):
    """Вьюсет дома"""
    queryset = House.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = HouseSerializer


class ApartmentViewSet(viewsets.ModelViewSet):
    """Вьюсет квартиры"""
    queryset = Apartment.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ApartmentSerializer
