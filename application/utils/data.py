import logging

import pandas

from enum import Enum

from django.db import DatabaseError

from api.exceptions import VehicleAPIException
from api.models import Vehicle
from api.serializers import VehicleSerializer
from utils.file import get_file_extension


class FileHeadersEnum(Enum):
    make = 'Марка'
    model = 'Модель'
    color = 'Цвет'
    registration_number = 'Регистрационный номер'
    year_of_manufacture = 'Год выпуска'
    vin = 'VIN'
    vehicle_certificate_number = 'Номер СТС'
    vehicle_certificate_date = 'Дата выдачи СТС'


def parse_vehicles(filename: str, data) -> list[dict]:
    """ Разбирает файл, содержащий информацию о транспортных средствах. """
    file_extension = get_file_extension(filename)

    if file_extension == 'csv':
        book = pandas.read_csv(data, encoding='cp1251', sep=';', quotechar='"')
    elif file_extension == 'xls':
        book = pandas.read_excel(data, sheet_name=0, header=0, engine='xlrd')
    elif file_extension == 'xlsx':
        book = pandas.read_excel(data, sheet_name=0, header=0, engine='openpyxl')
    else:
        raise VehicleAPIException(f'Неподдерживаемый тип файла "{file_extension}".')

    try:
        vehicles = []
        for _, row in book.iterrows():
            vehicle = dict()
            for item in FileHeadersEnum:
                # Изменить тип поля "Дата выдачи СТС" с Timestamp на Date (т.к. Pandas парсит дату в Timestamp)
                if item == FileHeadersEnum.vehicle_certificate_date and isinstance(row[item.value], pandas.Timestamp):
                    value = row[item.value].date()
                else:
                    value = row[item.value]
                vehicle[item.name] = value
            vehicles.append(vehicle)
    except KeyError as e:
        raise VehicleAPIException(f'Некорректный формат файла. Не найдена колонка данных: {e}')

    return vehicles


def save_vehicle(data: dict, **kwargs) -> Vehicle:
    print(f'Saving {data}')
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

    print(vehicle)
    return vehicle
