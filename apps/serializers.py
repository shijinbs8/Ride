from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import *


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user



class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = '__all__'

class RideCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['pickup_location', 'dropoff_location']

    def create(self, validated_data):
        validated_data['rider'] = self.context['request'].user
        return super().create(validated_data)
    

class RideStatusUpdateSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=Ride.STATUS_CHOICES)

    class Meta:
        model = Ride
        fields = ['status']

    def update(self, instance, validated_data):
        instance.status = validated_data['status']
        instance.save()
        return instance