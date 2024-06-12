from datetime import date

from celery import shared_task
from django.db.models import F, OuterRef, Subquery, Sum

from houses.models import Apartment, Rent, WaterMeter


@shared_task
def calculation_rent(house_id: int, month: int):
    """
    Расчет комунальных платежей.
    id_house - id дома в DB
    month - порядковый номер месяца от 1 до 12
    """
    prev_month_readings = WaterMeter.objects.filter(
            date__month=(month - 1),
            date__year=date.today().year,
            apartment=OuterRef('pk'),
            tariff=OuterRef('water_meter__tariff')
        )

    qw_st = (
            Apartment.objects.filter(house=house_id)
            .prefetch_related('water_meter')
            .filter(
                water_meter__date__month=month,
                water_meter__date__year=date.today().year
            ).alias(
                previous_value=Subquery(prev_month_readings.values('value')),
                cost=((F('water_meter__value') - F('previous_value'))
                      * F('water_meter__tariff'))
            ).values('number').annotate(cost_water=Sum('cost'),
                                        cost_property=F('area')
                                        * F('house__tariff_property__price'))
        )
    data = []
    # rent_list = 'Cписок квартплаты:'
    for value in qw_st:
        number = value.get('number')
        cost_water = value.get('cost_water')
        cost_property = value.get('cost_property')
        data.append(
            Rent(
                apartment=Apartment.objects.filter(number=number,
                                                   house=house_id)[0],
                cost_water=cost_water,
                cost_property=cost_property
            )
        )
        # rent_list += f'{number} = Вода{cost_water}р.; Исущество{cost_property}р.'
        
    rez_list: list[Rent] = Rent.objects.bulk_create(
        data,
        ignore_conflicts=True
    )
    rent_list
    print(rez_list)
