import logging

from rest_framework import views, status, generics, permissions
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from api.exceptions import VehicleAPIException
from api.filters import vehicle_list_filter
from api.models import Vehicle
from api.renderers import XLSXFileRenderer, CSVFileRenderer
from api.serializers import VehicleSerializer
from utils.data import (
    parse_vehicles, save_vehicle, file_type_from_content_type, CONTENT_TYPE_TO_FILE_TYPE_MAPPING,
    transform_vehicles, export_vehicles,
)


class ImportDataView(views.APIView):
    parser_classes = [FileUploadParser, ]
    permission_classes = [permissions.IsAuthenticated]

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


class ExportDataView(generics.ListAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = (JSONRenderer, XLSXFileRenderer, CSVFileRenderer, )

    def get(self, request, *args, **kwargs):
        # Определить тип запрашиваемого файла
        content_type = request.headers.get('Accept')
        try:
            file_type = file_type_from_content_type(content_type)
        except KeyError:
            error_message = f"""
                Указан некорректный или неподдерживаемый тип данных.\n
                Необходимо указать значение заголовка Accept, соответствующее формату передаваемого файла:\n
                {CONTENT_TYPE_TO_FILE_TYPE_MAPPING}
            """
            logging.error(error_message)
            raise VehicleAPIException(detail=error_message)

        match file_type:
            case 'xls':
                raise VehicleAPIException(detail=f'Выгрузка в формате {file_type} в данный момент не поддерживается.')
            case 'xlsx':
                data = export_vehicles(self.get_queryset(), file_type=file_type)
                response = Response(
                    data=data,
                    headers={'Content-Disposition': 'attachment; filename="vehicles.xlsx"', },
                    content_type=content_type,
                )
                return response
            case 'csv':
                data = export_vehicles(self.get_queryset(), file_type=file_type)
                response = Response(
                    data=data,
                    headers={'Content-Disposition': 'attachment; filename="vehicles.csv"', },
                    content_type=content_type,
                )
                return response

    def get_queryset(self):
        """ Реализует поиск данных по параметрам, переданным в запросе. """
        return vehicle_list_filter(self.request)
