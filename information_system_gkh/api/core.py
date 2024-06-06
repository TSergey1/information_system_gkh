from decimal import Decimal


def rent_property(flat_area: float, tariff: Decimal) -> Decimal:
    """Расчет стоимости содержания общего имущества."""

    return flat_area * tariff


def rent_water(meter_readings: int, tariff: Decimal) -> Decimal:
    """Расчет стоимости воды."""

    return meter_readings * tariff

# def all_rent(meter_readings: int, tariff: Decimal) -> Decimal:
#     """Расчет стоимости воды."""

#     return meter_readings * tariff
