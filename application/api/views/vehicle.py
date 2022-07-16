from rest_framework import generics
from rest_framework import permissions

from api.models import Vehicle, DATA_OPERATIONS_MAPPING
from api.serializers import VehicleSerializer
from utils.views import log_data_modification


class VehicleList(generics.ListCreateAPIView):
    """ API: Просмотр списка транспортных средств; Создание новой записи о транспортном средстве. """
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Создать новую запись
        response = self.create(request, *args, **kwargs)

        # Записать в лог информацию о создании новой записи
        log_data_modification(
            vehicle=response.data,
            username=request.user,
            operation=DATA_OPERATIONS_MAPPING['add'],
            description='Создана новая запись о транспортном средстве.',
        )

        return response

    def perform_create(self, serializer):
        """
        Переопределяет функцию perform_create класса CreateModelMixin.

        Внедряет данные, необходимые для создания новой записи.
        """
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def get_queryset(self):
        """ Реализует поиск данных по параметрам, переданным в запросе. """
        queryset = Vehicle.objects.all()

        # Получить параметры фильтрации из запроса
        make = self.request.query_params.get('make')
        model = self.request.query_params.get('model')
        color = self.request.query_params.get('color')
        registration_number = self.request.query_params.get('registration_number')
        year_of_manufacture = self.request.query_params.get('year_of_manufacture')
        vin = self.request.query_params.get('vin')
        vehicle_certificate_number = self.request.query_params.get('vehicle_certificate_number')
        vehicle_certificate_date = self.request.query_params.get('vehicle_certificate_date')

        # Сформировать фильтры по параметрам запроса
        filters = dict()

        if make is not None:
            filters['make__icontains'] = make
        if model is not None:
            filters['model__icontains'] = model
        if color is not None:
            filters['color__icontains'] = color
        if registration_number is not None:
            filters['registration_number__iexact'] = registration_number
        if year_of_manufacture is not None:
            filters['year_of_manufacture'] = year_of_manufacture
        if vin is not None:
            filters['vin__iexact'] = vin
        if vehicle_certificate_number is not None:
            filters['vehicle_certificate_number__iexact'] = vehicle_certificate_number
        if vehicle_certificate_date is not None:
            filters['vehicle_certificate_date'] = vehicle_certificate_date

        if filters:
            queryset = queryset.filter(**filters)

        return queryset


class VehicleDetail(generics.RetrieveUpdateDestroyAPIView):
    """ API: Просмотр выбранного транспортного средства; Редактирование и удаление записи о транспортном средстве. """
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        # Получить обновляемую запись
        vehicle = self.get_object()
        vehicle_data = VehicleSerializer(vehicle).data

        # Записать в лог информацию об обновлении существующей записи
        log_data_modification(
            vehicle=vehicle_data,
            username=request.user,
            operation=DATA_OPERATIONS_MAPPING['modify'],
            description='Изменена запись о транспортном средстве.',
        )

        # Обновить запись
        response = self.update(request, *args, **kwargs)

        return response

    def patch(self, request, *args, **kwargs):
        # Получить обновляемую запись
        vehicle = self.get_object()
        vehicle_data = VehicleSerializer(vehicle).data

        # Записать в лог информацию об обновлении существующей записи
        log_data_modification(
            vehicle=vehicle_data,
            username=request.user,
            operation=DATA_OPERATIONS_MAPPING['modify'],
            description='Изменена запись о транспортном средстве.',
        )

        # Обновить запись
        response = self.partial_update(request, *args, **kwargs)

        return response

    def delete(self, request, *args, **kwargs):
        # Получить удаляемую запись
        vehicle = self.get_object()
        vehicle_data = VehicleSerializer(vehicle).data

        # Записать в лог информацию об обновлении существующей записи
        log_data_modification(
            vehicle=vehicle_data,
            username=request.user,
            operation=DATA_OPERATIONS_MAPPING['remove'],
            description='Удалена запись о транспортном средстве.',
        )

        # Удалить запись
        response = self.destroy(request, *args, **kwargs)

        return response

    def perform_update(self, serializer):
        """
        Переопределяет функцию perform_update класса UpdateModelMixin.

        Внедряет данные, необходимые для обновления существующей записи.
        """
        serializer.save(updated_by=self.request.user)
