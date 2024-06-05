from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .serializers import HouseSerializer
from houses.models import House


class HouseViewSet(viewsets.ModelViewSet):
    """Вьюсет дома"""
    queryset = House.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = HouseSerializer
