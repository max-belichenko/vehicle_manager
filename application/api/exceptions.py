from rest_framework.exceptions import APIException


class VehicleAPIException(APIException):
    """ Базовое исключение приложения Vehicle API. """
    status_code = 500
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'service_unavailable'
