import logging

from rest_framework import views, status
from rest_framework.exceptions import APIException, ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response

from api.exceptions import VehicleAPIException
from utils.data import parse_vehicles, save_vehicle


class ImportDataView(views.APIView):
    parser_classes = [FileUploadParser]

    def put(self, request, filename, format=None):
        file_data = request.data['file']

        try:
            vehicles = parse_vehicles(filename, file_data)
        except VehicleAPIException as e:
            logging.warning(e)
            raise ParseError(detail=str(e))

        for vehicle in vehicles:
            save_vehicle(vehicle, created_by=request.user, updated_by=request.user)

        return Response(status=status.HTTP_201_CREATED)
