from rest_framework import serializers
from django.contrib.auth.models import User
from .models import RiderProfile, DriverProfile

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
