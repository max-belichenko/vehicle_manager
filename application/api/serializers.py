from django.contrib.auth.models import User, Group
from rest_framework import serializers

from api.models import Vehicle, DataLog


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """ Сериализатор модели User. """
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    """ Сериализатор модели Group. """
    class Meta:
        model = Group
        fields = ['url', 'name']


class VehicleSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели DataLog.

    Поля created_by и updated_by переопределены и отображают `User.username` вместо `User.id`.
    """
    created_by = serializers.SlugRelatedField(read_only=True, slug_field='username', )
    updated_by = serializers.SlugRelatedField(read_only=True, slug_field='username', )

    class Meta:
        model = Vehicle
        fields = ['id', 'created_at', 'created_by', 'updated_at', 'updated_by', 'make', 'model', 'color',
                  'registration_number', 'year_of_manufacture', 'vin', 'vehicle_certificate_number',
                  'vehicle_certificate_date', ]


class DataLogSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели DataLog.

    Поле created_by переопределено и отображает `User.username` вместо `User.id`.
    """
    created_by = serializers.SlugRelatedField(read_only=True, slug_field='username', )

    class Meta:
        model = DataLog
        fields = [
            'id', 'created_at', 'created_by', 'vehicle_id', 'registration_number', 'vin', 'vehicle_certificate_number',
            'operation', 'description',
        ]
        read_only_fields = [
            'id', 'created_at', 'created_by', 'vehicle_id', 'registration_number', 'vin', 'vehicle_certificate_number',
            'operation', 'description',
        ]
