from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (ApartmentViewSet, HouseViewSet, RentView,
                       WaterMeterViewSet)

router = DefaultRouter()

router.register(r'houses', HouseViewSet, basename='houses')
router.register(r'apartments', ApartmentViewSet, basename='apartments')
router.register(r'watermeters', WaterMeterViewSet, basename='water_meters')
# router.register(
#     r'houses/(?P<house_id>\d+)/month/(?P<month>\d+)',
#     RentViewSet,
#     basename='rent'
# )

urlpatterns = [
    path('', include(router.urls)),
    path(r'houses/<int:house_id>/month/<int:month>/',
         RentView.as_view(),
         name='rent'),
]
