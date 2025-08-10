from django.db import models
from django.contrib.auth.models import User

class Workplace(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    # Latitude and Longitude for mapping
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return self.name

class RiderProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='rider_profile')
    # As per BRD 3.1.4, user sets home and work addresses
    home_address = models.CharField(max_length=255)
    home_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    home_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    workplace = models.ForeignKey(Workplace, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Rider Profile"

class DriverProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver_profile')
    # Placeholder for driver-specific info
    phone_number_verified = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.user.username}'s Driver Profile"

class Vehicle(models.Model):
    # As per BRD 4.1
    driver = models.ForeignKey(DriverProfile, on_delete=models.CASCADE, related_name='vehicles', null=True, blank=True)
    vehicle_type = models.CharField(max_length=50) # e.g., 'Bus', 'Van', 'Car'
    capacity = models.PositiveSmallIntegerField()
    license_plate = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.license_plate} ({self.vehicle_type})"
