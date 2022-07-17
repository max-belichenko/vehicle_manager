from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

from api.validators import MaxCurrentYearValidator, ExactLengthValidator


# Константы
FIRST_CAR_MANUFACTURE_YEAR = 1886
VIN_LENGTH = 17
DATA_OPERATIONS_MAPPING = {
    'import': 'import',
    'export': 'export',
    'add': 'add',
    'modify': 'modify',
    'remove': 'remove',
    'get': 'get',
}
DATA_OPERATIONS = [
    (DATA_OPERATIONS_MAPPING['import'], 'Импорт'),
    (DATA_OPERATIONS_MAPPING['export'], 'Экспорт'),
    (DATA_OPERATIONS_MAPPING['add'], 'Добавить'),
    (DATA_OPERATIONS_MAPPING['modify'], 'Изменить'),
    (DATA_OPERATIONS_MAPPING['remove'], 'Удалить'),
    (DATA_OPERATIONS_MAPPING['get'], 'Получить'),
]


class Vehicle(models.Model):
    """ Транспортное средство """
    created_at = models.DateTimeField(
        verbose_name='Дата и время создания записи',
        auto_now_add=True,
    )
    created_by = models.ForeignKey(
        verbose_name='Пользователь, создавший запись',
        to=User,
        on_delete=models.DO_NOTHING,
        related_name='+',
    )
    updated_at = models.DateTimeField(
        verbose_name='Дата и время последнего изменения записи',
        auto_now=True,
    )
    updated_by = models.ForeignKey(
        verbose_name='Пользователь, изменивший запись',
        to=User,
        on_delete=models.DO_NOTHING,
        related_name='+',
    )

    make = models.CharField(
        verbose_name='Марка',
        help_text='Марка (производитель) автомобиля',
        max_length=100,
    )
    model = models.CharField(
        verbose_name='Модель',
        help_text='Модель автомобиля',
        max_length=255,
    )
    color = models.CharField(
        verbose_name='Цвет',
        help_text='Цвет автомобиля',
        max_length=100,
    )
    registration_number = models.CharField(
        verbose_name='Регистрационный номер',
        help_text='Российский или иностранный государственный регистрационный номер автомобиля',
        max_length=100,
        unique=True,
    )
    year_of_manufacture = models.IntegerField(
        verbose_name='Год выпуска',
        help_text=f'Год выпуска автомобиля. Должен быть в диапазоне от {FIRST_CAR_MANUFACTURE_YEAR} '
                  f'до текущего года включительно.',
        validators=[MinValueValidator(FIRST_CAR_MANUFACTURE_YEAR), MaxCurrentYearValidator],
    )
    vin = models.CharField(
        verbose_name='VIN',
        help_text='VIN-номер (идентификационный номер транспортного средства), состоит из 17 знаков.',
        max_length=VIN_LENGTH,
        validators=[ExactLengthValidator(VIN_LENGTH), ],
        unique=True,
    )
    vehicle_certificate_number = models.CharField(
        verbose_name='Номер СТС',
        help_text='Свидетельство о регистрации транспортного средства.',
        max_length=100,
        unique=True,
    )
    vehicle_certificate_date = models.DateField(
        verbose_name='Дата выдачи СТС',
        help_text='Дата выдачи свидетельства о регистрации транспортного средства.',
    )

    def __str__(self):
        return f'{self.make} {self.model} ({self.registration_number})'

    class Meta:
        ordering = ('make', 'model', )
        verbose_name = 'Транспортное средство'
        verbose_name_plural = 'Транспортные средства'


class DataLog(models.Model):
    """ Лог доступа к данным транспортных средств """
    created_at = models.DateTimeField(
        verbose_name='Дата и время создания записи',
        auto_now_add=True,
    )
    created_by = models.ForeignKey(
        verbose_name='Пользователь, создавший запись',
        to=User,
        on_delete=models.DO_NOTHING,
        related_name='+',
    )

    vehicle_id = models.BigIntegerField(
        verbose_name='ID записи о транспортном средстве',
    )
    registration_number = models.CharField(
        verbose_name='Регистрационный номер',
        help_text='Российский или иностранный государственный регистрационный номер автомобиля',
        max_length=100,
    )
    vin = models.CharField(
        verbose_name='VIN',
        help_text='VIN-номер (идентификационный номер транспортного средства), состоит из 17 знаков.',
        max_length=VIN_LENGTH,
        validators=[ExactLengthValidator(VIN_LENGTH), ]
    )
    vehicle_certificate_number = models.CharField(
        verbose_name='Номер СТС',
        help_text='Свидетельство о регистрации транспортного средства.',
        max_length=100,
    )

    operation = models.CharField(
        verbose_name='Операция',
        help_text='Операция над данными (импорт/экспорт).',
        max_length=100,
        choices=DATA_OPERATIONS,
    )
    description = models.CharField(
        verbose_name='Описание операции',
        help_text='Детализированная информация по операции.',
        max_length=100,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'{self.operation} {self.registration_number} ({self.description})'

    class Meta:
        ordering = ('-created_at', )
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
