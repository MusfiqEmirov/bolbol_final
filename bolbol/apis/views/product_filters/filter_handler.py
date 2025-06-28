from django.db.models import Q, QuerySet
from typing import Dict
from products.models import Product


def filter_transport_characteristics(qs: QuerySet[Product], characteristics: Dict) -> QuerySet[Product]:
    """
    Filters transport-related products based on their characteristics.
    """

    brand = characteristics.get("brand")
    model = characteristics.get("model")
    color = characteristics.get("color")
    fuel_type = characteristics.get("fuel_type")
    body_type = characteristics.get("body_type")
    engine_volume_min = characteristics.get("engine_volume_min")
    engine_volume_max = characteristics.get("engine_volume_max")
    year_min = characteristics.get("year_min")
    year_max = characteristics.get("year_max")
    transmission = characteristics.get("transmission")
    car_condition = characteristics.get("car_condition")
    mileage_min = characteristics.get("mileage_min")
    mileage_max = characteristics.get("mileage_max")
    drivetrain = characteristics.get("drivetrain")
    seat_count = characteristics.get("seat_count")
    engine_power_min = characteristics.get("engine_power_min")
    engine_power_max = characteristics.get("engine_power_max")
    additional_features = characteristics.get("additional_features", [])

    if brand:
        qs = qs.filter(characteristics__brand__iexact=brand)
    if model:
        qs = qs.filter(Q(characteristics__model__iexact=model))
    if color:
        qs = qs.filter(Q(characteristics__color__iexact=color))
    if fuel_type:
        qs = qs.filter(Q(characteristics__fuel_type__iexact=fuel_type))
    if body_type:
        qs = qs.filter(Q(characteristics__body_type__iexact=body_type))
    if engine_volume_min is not None:
        qs = qs.filter(Q(characteristics__engine_volume_min__gte=engine_volume_min))
    if engine_volume_max is not None:
        qs = qs.filter(Q(characteristics__engine_volume_max__lte=engine_volume_max))
    if year_min is not None:
        qs = qs.filter(Q(characteristics__year_min__gte=year_min))
    if year_max is not None:
        qs = qs.filter(Q(characteristics__year_max__lte=year_max))
    if transmission:
        qs = qs.filter(Q(characteristics__transmission__iexact=transmission))
    if car_condition:
        qs = qs.filter(Q(characteristics__car_condition__iexact=car_condition))
    if mileage_min is not None:
        qs = qs.filter(Q(characteristics__mileage_min__gte=mileage_min))
    if mileage_max is not None:
        qs = qs.filter(Q(characteristics__mileage_max__lte=mileage_max))
    if drivetrain:
        qs = qs.filter(Q(characteristics__drivetrain__iexact=drivetrain))
    if seat_count is not None:
        qs = qs.filter(Q(characteristics__seat_count=seat_count))
    if engine_power_min is not None:
        qs = qs.filter(Q(characteristics__engine_power_min__gte=engine_power_min))
    if engine_power_max is not None:
        qs = qs.filter(Q(characteristics__engine_power_max__lte=engine_power_max))
    if additional_features:
        for feature in additional_features:
            qs = qs.filter(
                Q(characteristics__additional_features__icontains=feature)
            )

    return qs