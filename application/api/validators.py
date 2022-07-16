from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator

from utils.validators import get_current_year


def MaxCurrentYearValidator(value: int):
    """ Проверяет, что указанный год меньше или равен текущему году. """
    current_year = get_current_year()

    if value > current_year:
        raise ValidationError(
            'Указанный год %(value)s больше текущего года %(current_year)s',
            params={'value': value, 'current_year': current_year},
        )


class ExactLengthValidator(BaseValidator):
    """ Проверяет, что строка имеет ровно указанную длину. """

    message = "Строка должна содержать ровно %(limit_value)d символов."
    code = "exact_length"

    def compare(self, a, b):
        return a != b

    def clean(self, x):
        return len(x)
