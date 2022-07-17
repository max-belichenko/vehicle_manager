import logging

from rest_framework import views, status
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response

from api.exceptions import VehicleAPIException
from utils.data import parse_vehicles, save_vehicle, file_type_from_content_type, CONTENT_TYPE_TO_FILE_TYPE_MAPPING, \
    transform_vehicles


class ImportDataView(views.APIView):
    parser_classes = [FileUploadParser, ]

    def put(self, request):
        file_data = request.data['file']

        # Определить тип полученного файла
        try:
            file_type = file_type_from_content_type(request.content_type)
        except KeyError:
            error_message = f"""
                Указан некорректный или неподдерживаемый тип данных.\n
                Необходимо указать значение заголовка Content-Type, соответствующее формату передаваемого файла:\n
                {CONTENT_TYPE_TO_FILE_TYPE_MAPPING}
            """
            logging.error(error_message)
            raise VehicleAPIException(error_message)

        # Разобрать файл и получить данные
        try:
            vehicles = parse_vehicles(file_type, file_data)
        except VehicleAPIException as e:
            raise ParseError(detail=str(e))

        # Подготовить данные для сохранения в БД
        vehicles = transform_vehicles(vehicles)

        # Сохранить данные в БД
        for vehicle in vehicles:
            save_vehicle(vehicle, created_by=request.user, updated_by=request.user)

        return Response(status=status.HTTP_201_CREATED)
