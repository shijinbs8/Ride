import math

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points on the Earth's surface.
    
    Parameters:
        lat1, lon1: Latitude and longitude of the first point (in decimal degrees).
        lat2, lon2: Latitude and longitude of the second point (in decimal degrees).
    
    Returns:
        Distance in kilometers.
    """
    R = 6371  # Radius of Earth in kilometers

    # Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Difference in coordinates
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Haversine formula
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distance in kilometers
    distance = R * c
    return distance
from .models import Ride, DriverProfile
from django.db.models import Q

def find_nearby_drivers(rider, radius=5.0):
    """
    Finds nearby available drivers based on proximity to the rider's location.
    
    Parameters:
        rider: The rider object requesting the ride.
        radius: The maximum radius in kilometers within which to find drivers (default is 5 km).
    
    Returns:
        A list of drivers within the specified radius.
    """
    # Get the rider's pickup location (latitude and longitude)
    rider_lat, rider_lon = map(float, rider.profile.location.split(','))

    # Get all drivers' profiles who are available (drivers without an ongoing ride)
    available_drivers = DriverProfile.objects.filter(is_driver=True)

    nearby_drivers = []

    for driver_profile in available_drivers:
        # Get the driver's location (latitude and longitude)
        driver_lat, driver_lon = map(float, driver_profile.location.split(','))

        # Calculate the distance between the rider and the driver
        distance = haversine(rider_lat, rider_lon, driver_lat, driver_lon)

        # If the distance is within the specified radius, add the driver to the list
        if distance <= radius:
            nearby_drivers.append((driver_profile, distance))

    # Sort the nearby drivers by distance (ascending order)
    nearby_drivers.sort(key=lambda x: x[1])

    return nearby_drivers
def match_ride_with_driver(ride):
    """
    Matches a ride request with the closest available driver within a given radius.
    
    Parameters:
        ride: The ride request object.
    
    Returns:
        A tuple containing the matched driver and the updated ride.
    """
    # Find the nearby drivers within a radius of 5 km (you can adjust this radius)
    nearby_drivers = find_nearby_drivers(ride.rider, radius=5.0)

    if not nearby_drivers:
        # No nearby drivers found
        return None, None

    # Select the closest available driver
    closest_driver, distance = nearby_drivers[0]

    # Assign the ride to the closest driver
    ride.driver = closest_driver.user
    ride.status = 'accepted'
    ride.save()

    return closest_driver, ride
