from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import ApartmentViewSet, HouseViewSet, WaterMeterViewSet

router = DefaultRouter()

router.register(r'houses', HouseViewSet, basename='houses')
router.register(r'apartments', ApartmentViewSet, basename='apartments')
router.register(r'watermeters', WaterMeterViewSet, basename='water_meters')

urlpatterns = [
    path('', include(router.urls)),
]
