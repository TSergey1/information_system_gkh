from api.serializers import EventSerializer
from celery import shared_task

from houses.models import Apartment, Tariff


@shared_task
def communal_payments(id_house: int, month: int):
    """
    Расчет комунальных платежей.
    id_house - id дома из БД
    month - порядковый номер месяца от 1 до 12
    """
    tariff = Tariff.objects.all()
    apartment = Apartment.objects.filter(house=id_house)
