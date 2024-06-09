from datetime import datetime
#  celery import shared_task

from .core import rent_property, rent_water
from houses.models import Apartment, Tariff


@shared_task
def start_calculation(id_house: int, month: int):
    """
    Расчет комунальных платежей.
    id_house - id дома в DB
    month - порядковый номер месяца от 1 до 12
    """
    result = {}
    tariff = Tariff.objects.all()
    apartments = Apartment.objects.select_related(
        'water_meter',
        'water_meter__value'
    ).filter(
        house=id_house,
        water_meter__value__date__range=(
            datetime.date(datetime.now().year, month-1, 1),
            datetime.date(datetime.now().year, month, 1)
        )
    )
    print(apartments)
