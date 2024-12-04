from django.db import models
from django.contrib.auth.models import User

class DriverProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_driver = models.BooleanField(default=False)
    location = models.CharField(max_length=255, null=True, blank=True)  # Simulated location

    def __str__(self):
        return f"Driver Profile for {self.user.username}"

class Ride(models.Model):
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('accepted', 'Accepted'),
        ('started', 'Started'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    rider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rides_as_rider')
    driver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='rides_as_driver')
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
    created_at = models.DateTimeField(auto_now_add=True)
    current_location = models.CharField(max_length=255, null=True, blank=True)  # Simulate current location
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ride {self.id} - {self.status}"

    def update_status(self, new_status):
        if new_status not in dict(self.STATUS_CHOICES):
            raise ValueError(f"Invalid status: {new_status}")
        self.status = new_status
        self.save()

    def update_location(self, latitude, longitude):
        # Update the current location with latitude and longitude as 'latitude,longitude'
        self.current_location = f"{latitude},{longitude}"
        self.save()

    def get_latitude(self):
        # Parse the current location to get latitude
        if self.current_location:
            return float(self.current_location.split(',')[0])
        return None

    def get_longitude(self):
        # Parse the current location to get longitude
        if self.current_location:
            return float(self.current_location.split(',')[1])
        return None

