from attr import fields
from rest_framework import serializers

from .models import (
    Cars,Route,Schedules, Passengers, Sacco
)

class SaccoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sacco
        fields = '__all__'

class Carserializer(serializers.ModelSerializer):

    sacco_data = SaccoSerializer(read_only=True, source='sacco')

    class Meta:
        model = Cars
        fields = ['id', 'sacco_data', 'plate_name', 'plate_number', 'seats']

class Routeserializer(serializers.ModelSerializer):

    class Meta:
        model = Route
        fields = '__all__'

class Scheduleserializer(serializers.ModelSerializer):

    car_data = Carserializer(read_only=True, source='car')
    route = Routeserializer(read_only=True, source='routes')

    class Meta:
        model = Schedules
        fields = ['id', 'car_data', 'route', 'date', 'time', 'price', 'full', 'occupied_seats']

class Passengerserializer(serializers.ModelSerializer):

    class Meta:
        model = Passengers
        fields = '__all__'