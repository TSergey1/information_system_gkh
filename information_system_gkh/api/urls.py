from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import HouseViewSet

router = DefaultRouter()

router.register(r'houses', HouseViewSet, basename='houses')

urlpatterns = [
    path('', include(router.urls)),
]
