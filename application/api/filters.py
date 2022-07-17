from django.db.models import QuerySet
from rest_framework.request import Request

from api.models import Vehicle
from utils.views import build_field_lookup


def vehicle_list_filter(request: Request) -> QuerySet:
    """
    Реализует фильтрацию списка транспортных средств по предоставленным параметрам.
    Возвращает отфильтрованный список записей.
    """

    # Сформировать фильтры по параметрам запроса
    filters = dict()
    filters.update(build_field_lookup(request=request, parameter='make', filtering_method='icontains'))
    filters.update(build_field_lookup(request=request, parameter='model', filtering_method='icontains'))
    filters.update(build_field_lookup(request=request, parameter='color', filtering_method='icontains'))
    filters.update(
        build_field_lookup(request=request, parameter='registration_number', filtering_method='iexact'))
    filters.update(build_field_lookup(request=request, parameter='year_of_manufacture'))
    filters.update(build_field_lookup(request=request, parameter='vin', filtering_method='iexact'))
    filters.update(
        build_field_lookup(request=request, parameter='vehicle_certificate_number', filtering_method='iexact'))
    filters.update(build_field_lookup(request=request, parameter='vehicle_certificate_date'))

    if filters:
        queryset = Vehicle.objects.filter(**filters)
    else:
        queryset = Vehicle.objects.all()

    return queryset
