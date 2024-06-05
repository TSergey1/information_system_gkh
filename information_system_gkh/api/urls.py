from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import ApartmentViewSet, HouseViewSet

router = DefaultRouter()

router.register(r'houses', HouseViewSet, basename='houses')
router.register(r'apartments', ApartmentViewSet, basename='apartments')

urlpatterns = [
    path('', include(router.urls)),
]
