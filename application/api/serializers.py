from django.contrib.auth.models import User, Group
from rest_framework import serializers

from api.exceptions import VehicleAPIException
from api.models import Vehicle, DataLog


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class VehicleSerializer(serializers.ModelSerializer):
    # Переопределить сериализацию некоторых полей
    created_by = serializers.SlugRelatedField(read_only=True, slug_field='username', )  # Отображать username вместо id
    updated_by = serializers.SlugRelatedField(read_only=True, slug_field='username', )  # Отображать username вместо id

    def create(self, validated_data):
        """
        Создаёт и возвращает новый объект Vehicle.
        """
        try:
            user = self.context['request'].user
        except KeyError:
            raise VehicleAPIException(
                'VehicleSerializer: Необходимо передать Request, как дополнительный контекст. Пример: '
                'VehicleSerializer(validated_data, context={\'request\': request})'
            )

        validated_data['created_by'] = user
        validated_data['updated_by'] = user

        return Vehicle.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Обновляет и возвращает существующий объект Vehicle.
        """
        try:
            user = self.context['request'].user
        except KeyError:
            raise VehicleAPIException(
                'VehicleSerializer: Необходимо передать Request, как дополнительный контекст. Пример: '
                'VehicleSerializer(validated_data, context={\'request\': request})'
            )

        instance.updated_by = user
        instance.make = validated_data.get('make', instance.make)
        instance.model = validated_data.get('model', instance.model)
        instance.color = validated_data.get('color', instance.color)
        instance.registration_number = validated_data.get('registration_number', instance.registration_number)
        instance.year_of_manufacture = validated_data.get('year_of_manufacture', instance.year_of_manufacture)
        instance.vin = validated_data.get('vin', instance.vin)
        instance.vehicle_certificate_number = validated_data.get('vehicle_certificate_number', instance.vehicle_certificate_number)
        instance.vehicle_certificate_date = validated_data.get('vehicle_certificate_date', instance.vehicle_certificate_date)
        instance.save()
        return instance

    class Meta:
        model = Vehicle
        fields = ['id', 'created_at', 'created_by', 'updated_at', 'updated_by', 'make', 'model', 'color',
                  'registration_number', 'year_of_manufacture', 'vin', 'vehicle_certificate_number',
                  'vehicle_certificate_date', ]


class DataLogSerializer(serializers.ModelSerializer):
    # Переопределить сериализацию некоторых полей
    created_by = serializers.SlugRelatedField(read_only=True, slug_field='username', )  # Отображать username вместо id

    def create(self, validated_data):
        """
        Создаёт и возвращает новый объект Vehicle.
        """
        try:
            user = self.context['request'].user
        except KeyError:
            raise VehicleAPIException(
                'VehicleSerializer: Необходимо передать Request, как дополнительный контекст. Пример: '
                'VehicleSerializer(validated_data, context={\'request\': request})'
            )

        validated_data['created_by'] = user

        return DataLog.objects.create(**validated_data)

    class Meta:
        model = DataLog
        fields = ['id', 'created_at', 'created_by', 'vehicle_id', 'registration_number', 'vin',
                  'vehicle_certificate_number', 'operation', 'description', ]
        read_only_fields = ['id', 'created_at', 'created_by', 'vehicle_id', 'registration_number', 'vin',
                            'vehicle_certificate_number', 'operation', 'description', ]
