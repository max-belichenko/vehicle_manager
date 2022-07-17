import logging
from typing import Optional

import pandas

from enum import Enum

from django.db import DatabaseError

from api.exceptions import VehicleAPIException
from api.models import Vehicle
from api.serializers import VehicleSerializer


CONTENT_TYPE_TO_FILE_TYPE_MAPPING = {
    'text/csv': 'csv',
    'application/vnd.ms-excel': 'xls',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'xlsx',
}


def file_type_from_content_type(content_type: str) -> Optional[str]:
    """ Определяет тип переданного файла по содержимому заголовка Content-Type. """
    return CONTENT_TYPE_TO_FILE_TYPE_MAPPING[content_type]


class FileHeadersEnum(Enum):
    """ Названия столбцов данных в файле, содержащем информацию о транспортных средствах. """
    make = 'Марка'
    model = 'Модель'
    color = 'Цвет'
    registration_number = 'Регистрационный номер'
    year_of_manufacture = 'Год выпуска'
    vin = 'VIN'
    vehicle_certificate_number = 'Номер СТС'
    vehicle_certificate_date = 'Дата выдачи СТС'


def read_data_to_dataframe(file_type: str, data) -> pandas.DataFrame:
    """ Читает файл (или другой поддерживаемый источник данных) в Pandas DataFrame. """
    match file_type:
        case 'csv':
            dataframe = pandas.read_csv(data, encoding='cp1251', sep=';', quotechar='"')
        case 'xls':
            dataframe = pandas.read_excel(data, sheet_name=0, header=0, engine='xlrd')
        case 'xlsx':
            dataframe = pandas.read_excel(data, sheet_name=0, header=0, engine='openpyxl')
        case _:
            raise ValueError(f'Формат файла {file_type} не поддерживается.')

    return dataframe


def parse_vehicles(file_type: str, data) -> list[dict]:
    """ Разбирает файл, содержащий информацию о транспортных средствах. """
    try:
        dataframe = read_data_to_dataframe(file_type, data)
    except ValueError as e:
        raise VehicleAPIException(f'Не удалось преобразовать данные в DataFrame: {e}')

    vehicles = []
    for _, row in dataframe.iterrows():
        vehicle = dict()
        for item in FileHeadersEnum:
            try:
                # Изменить тип поля "Дата выдачи СТС" с `Timestamp` на `date` (т.к. Pandas трактует дату как Timestamp)
                if item == FileHeadersEnum.vehicle_certificate_date and isinstance(row[item.value], pandas.Timestamp):
                    value = row[item.value].date()
                else:
                    value = row[item.value]
            except KeyError as e:
                raise VehicleAPIException(f'Некорректный формат файла. Не найдена колонка данных: {e}')
            vehicle[item.name] = value
        vehicles.append(vehicle)

    return vehicles


def save_vehicle(data: dict, **kwargs) -> Vehicle:
    """
    Сохраняет информацию о транспортном средстве в базу данных.

    Внедряет дополнительные поля из `kwargs` при сохранении.
    """
    serializer = VehicleSerializer(data=data)
    if serializer.is_valid():
        try:
            vehicle = serializer.save(**kwargs)
        except DatabaseError as e:
            error_message = f'При попытке записать данные о транспортном средстве возникла ошибка:\n'\
                            f'Данные: {serializer.data}\n'\
                            f'Ошибка: {e}'
            logging.error(error_message)
            raise VehicleAPIException(error_message)
    else:
        raise VehicleAPIException(f'Некорректный формат данных: {serializer.errors}')

    return vehicle
