from rest_framework import generics
from rest_framework import permissions

from api.models import DataLog
from api.serializers import DataLogSerializer


class DataLogView(generics.ListAPIView):
    """ API: просмотр лога доступа к данным о транспортных средствах. """
    queryset = DataLog.objects.all()
    serializer_class = DataLogSerializer
    permission_classes = [permissions.IsAdminUser]
