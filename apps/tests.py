from django.test import TestCase
from django.contrib.auth.models import User
from .models import Ride, DriverProfile

class RideModelTest(TestCase):

    def setUp(self):
        # Create users
        self.rider = User.objects.create_user(username='rider', password='testpassword')
        self.driver = User.objects.create_user(username='driver', password='testpassword')

        # Create driver profile for the driver
        self.driver_profile = DriverProfile.objects.create(user=self.driver, is_driver=True)

        # Create a ride request
        self.ride = Ride.objects.create(
            rider=self.rider,
            pickup_location="Location A",
            dropoff_location="Location B"
        )

    def test_ride_creation(self):
        """Test creating a new ride."""
        ride = Ride.objects.create(
            rider=self.rider,
            pickup_location="New Pickup Location",
            dropoff_location="New Dropoff Location"
        )
        self.assertEqual(ride.rider, self.rider)
        self.assertEqual(ride.pickup_location, "New Pickup Location")
        self.assertEqual(ride.status, "requested")
    
    def test_update_status(self):
        """Test updating the ride status."""
        self.ride.update_status("accepted")
        self.ride.refresh_from_db()
        self.assertEqual(self.ride.status, "accepted")
    
    def test_invalid_status_update(self):
        """Test invalid status update."""
        with self.assertRaises(ValueError):
            self.ride.update_status("invalid_status")
    
    def test_ride_driver_assignment(self):
        """Test assigning a driver to the ride."""
        self.ride.driver = self.driver
        self.ride.save()
        self.ride.refresh_from_db()
        self.assertEqual(self.ride.driver, self.driver)

class DriverProfileModelTest(TestCase):

    def setUp(self):
        # Create users
        self.user = User.objects.create_user(username='driver', password='testpassword')
        self.driver_profile = DriverProfile.objects.create(user=self.user, is_driver=True)

    def test_driver_profile_creation(self):
        """Test creating a driver profile."""
        self.assertEqual(self.driver_profile.user.username, 'driver')
        self.assertTrue(self.driver_profile.is_driver)
