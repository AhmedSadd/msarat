from rest_framework import serializers
from django.contrib.auth.models import User
from .models import RiderProfile, DriverProfile, Workplace, Vehicle

class VehicleSerializer(serializers.ModelSerializer):
    driver_username = serializers.CharField(source='driver.user.username', read_only=True)

    class Meta:
        model = Vehicle
        fields = ('id', 'driver', 'driver_username', 'vehicle_type', 'capacity', 'license_plate')

class DriverProfileSerializer(serializers.ModelSerializer):
    # Include fields from the User model for creation and reading
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name', allow_blank=True, required=False)
    last_name = serializers.CharField(source='user.last_name', allow_blank=True, required=False)

    # Password is write-only for creation
    password = serializers.CharField(write_only=True)

    class Meta:
        model = DriverProfile
        fields = ('id', 'user', 'username', 'email', 'first_name', 'last_name', 'password', 'phone_number_verified')
        read_only_fields = ('user',)

    def create(self, validated_data):
        user_data = validated_data.pop('user', {})
        password = validated_data.pop('password')

        # Create the User instance
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data.get('email', ''),
            password=password,
            first_name=user_data.get('first_name', ''),
            last_name=user_data.get('last_name', '')
        )

        # Create the DriverProfile instance
        driver_profile = DriverProfile.objects.create(user=user, **validated_data)
        return driver_profile

class WorkplaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workplace
        fields = '__all__'

class RiderProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiderProfile
        fields = ('home_address', 'home_latitude', 'home_longitude', 'workplace')

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        # Default to creating a RiderProfile for every new user.
        # This can be adjusted later if there's a specific role selection.
        RiderProfile.objects.create(user=user)
        return user
