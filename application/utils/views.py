import logging
from typing import Optional

from django.db import DatabaseError
from rest_framework.request import Request

from api.models import DataLog


def log_data_modification(vehicle: dict, username: str, operation: str, description: str):
    """ Сохраняет запись в лог-таблице об изменении данных по транспортному средству. """
    try:
        log = DataLog.objects.create(
            created_by=username,
            operation=operation,
            description=description,
            vehicle_id=vehicle['id'],
            registration_number=vehicle['registration_number'],
            vin=vehicle['vin'],
            vehicle_certificate_number=vehicle['vehicle_certificate_number'],
        )
        log.save()
    except DatabaseError as e:
        error_message = f'При попытке записать данные в лог-таблицу возникла ошибка: {e}'
        logging.warning(error_message)


def build_field_lookup(request: Request, parameter: str, filtering_method: Optional[str] = None) -> dict:
    value = request.query_params.get(parameter)

    if value is None:
        field_lookup = {}
    else:
        field_lookup_query = f'{parameter}'
        if filtering_method:
            field_lookup_query += f'__{filtering_method}'
        field_lookup = {field_lookup_query: value}

    return field_lookup
