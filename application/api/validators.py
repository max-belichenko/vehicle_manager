from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator

from utils.validators import get_current_year


def MaxCurrentYearValidator(value: int):
    """ Validates that value is less or equal than current year. """
    current_year = get_current_year()

    if value > current_year:
        raise ValidationError(
            'Указанный год %(value)s больше текущего года %(current_year)s',
            params={'value': value, 'current_year': current_year},
        )


class ExactLengthValidator(BaseValidator):
    """ Validates that value string of exactly specified length. """

    message = "Строка должна содержать ровно %(limit_value)d символов."
    code = "exact_length"

    def compare(self, a, b):
        return a != b

    def clean(self, x):
        return len(x)
