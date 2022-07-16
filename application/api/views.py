from django.contrib.auth.models import User, Group

from rest_framework import viewsets, generics
from rest_framework import permissions

from api.models import Vehicle, DATA_OPERATIONS_MAPPING
from api.serializers import UserSerializer, GroupSerializer, VehicleSerializer
from utils.views import log_data_modification


class UserViewSet(viewsets.ModelViewSet):
    """ API: просмотр и редактирование пользователей. """
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class GroupViewSet(viewsets.ModelViewSet):
    """ API: просмотр и редактирование групп. """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAdminUser]


class VehicleList(generics.ListCreateAPIView):
    """ API: Просмотр списка транспортных средств; Создание новой записи о транспортном средстве. """
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

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


class VehicleDetail(generics.RetrieveUpdateDestroyAPIView):
    """ API: Просмотр выбранного транспортного средства; Редактирование и удаление записи о транспортном средстве. """
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

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
