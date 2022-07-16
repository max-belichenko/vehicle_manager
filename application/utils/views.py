import logging

from django.db import DatabaseError

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
