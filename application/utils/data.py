import datetime
import logging
import pandas

from django.db import DatabaseError
from enum import Enum
from typing import Optional

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
            error_message = f'Формат файла {file_type} не поддерживается.'
            logging.error(error_message)
            raise ValueError(error_message)

    return dataframe


def parse_vehicles(file_type: str, data) -> list[dict]:
    """ Разбирает файл, содержащий информацию о транспортных средствах. """
    logging.debug(f'parse_vehicles({file_type=}, {data=})')

    try:
        dataframe = read_data_to_dataframe(file_type, data)
    except ValueError as e:
        error_message = f'Не удалось преобразовать данные в DataFrame: {e}'
        logging.error(error_message)
        raise VehicleAPIException(error_message)

    try:
        vehicles = [
            {item.name: row[item.value] for item in FileHeadersEnum}
            for _, row in dataframe.iterrows()
        ]
    except KeyError as e:
        error_message = f'Некорректный формат файла. Не найдена колонка данных: {e}'
        logging.error(error_message)
        raise VehicleAPIException(error_message)

    return vehicles


def transform_vehicles(data: list[dict]) -> list[dict]:
    """ Производит необходимые преобразования данных, подготавливая их к последующему сохранению в БД. """
    logging.debug(f'transform_vehicles({data=})')

    # Преобразовать тип данных для колонки 'Дата выдачи СТС' из Timestamp или datetime в date.
    key = FileHeadersEnum.vehicle_certificate_date.name     # Соответствует колонке 'Дата выдачи СТС'
    for item in data:
        value = item[key]
        if isinstance(value, (pandas.Timestamp, datetime.datetime)):
            value = value.date()
            item[key] = value

    return data


def save_vehicle(data: dict, **kwargs) -> Vehicle:
    """
    Сохраняет информацию о транспортном средстве в базу данных.

    Внедряет дополнительные поля из `kwargs` при сохранении.
    """
    logging.debug(f'save_vehicle({data=})')

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
        error_message = f'Некорректный формат данных: {serializer.errors}'
        logging.error(error_message)
        raise VehicleAPIException(error_message)

    return vehicle
