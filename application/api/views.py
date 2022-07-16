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
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)
        log_data_modification(
            vehicle=response.data,
            username=request.user,
            operation=DATA_OPERATIONS_MAPPING['add'],
            description='Создана новая запись о транспортном средстве.',
        )
        return response

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)


class VehicleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    def put(self, request, *args, **kwargs):
        vehicle = self.get_object()
        vehicle_data = VehicleSerializer(vehicle).data
        log_data_modification(
            vehicle=vehicle_data,
            username=request.user,
            operation=DATA_OPERATIONS_MAPPING['modify'],
            description='Изменена запись о транспортном средстве.',
        )
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        vehicle = self.get_object()
        vehicle_data = VehicleSerializer(vehicle).data
        log_data_modification(
            vehicle=vehicle_data,
            username=request.user,
            operation=DATA_OPERATIONS_MAPPING['modify'],
            description='Изменена запись о транспортном средстве.',
        )
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        vehicle = self.get_object()
        vehicle_data = VehicleSerializer(vehicle).data
        log_data_modification(
            vehicle=vehicle_data,
            username=request.user,
            operation=DATA_OPERATIONS_MAPPING['remove'],
            description='Удалена запись о транспортном средстве.',
        )
        return self.destroy(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

#
#
# class VehicleList(APIView):
#     """
#     List all snippets, or create a new snippet.
#     """
#     def get(self, request):
#         vehicles = Vehicle.objects.all()
#         serializer = VehicleSerializer(vehicles, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = VehicleSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             response = Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#         return response
#
#
# class VehicleDetail(APIView):
#     """
#     Retrieve, update or delete a snippet instance.
#     """
#     def get_object(self, pk):
#         try:
#             return Vehicle.objects.get(pk=pk)
#         except Vehicle.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk):
#         vehicle = self.get_object(pk)
#         serializer = VehicleSerializer(vehicle)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         vehicle = self.get_object(pk)
#         serializer = VehicleSerializer(vehicle, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             response = Response(serializer.data)
#         else:
#             response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#         return response
#
#     def delete(self, request, pk):
#         vehicle = self.get_object(pk)
#         vehicle.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
