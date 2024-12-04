from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework import status, permissions
import math
import random
from time import sleep
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated




class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RideCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = RideCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            ride = serializer.save()
            return Response(RideSerializer(ride).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RideDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            ride = Ride.objects.get(pk=pk)
            return Response(RideSerializer(ride).data, status=status.HTTP_200_OK)
        except Ride.DoesNotExist:
            return Response({"error": "Ride not found"}, status=status.HTTP_404_NOT_FOUND)


class RideListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        rides = Ride.objects.all()
        serializer = RideSerializer(rides, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class RideStatusUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        try:
            ride = Ride.objects.get(pk=pk)
        except Ride.DoesNotExist:
            return Response({"error": "Ride not found"}, status=status.HTTP_404_NOT_FOUND)

        # Optional: Check if the user is authorized to update the status
        if ride.rider != request.user and ride.driver != request.user:
            return Response({"error": "You are not authorized to update this ride"}, status=status.HTTP_403_FORBIDDEN)

        serializer = RideStatusUpdateSerializer(ride, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RideLocationUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        try:
            ride = Ride.objects.get(pk=pk)
        except Ride.DoesNotExist:
            return Response({"error": "Ride not found"}, status=status.HTTP_404_NOT_FOUND)

        # Optional: Check if the user is authorized to update the location
        if ride.rider != request.user and ride.driver != request.user:
            return Response({"error": "You are not authorized to update this ride"}, status=status.HTTP_403_FORBIDDEN)

        # Check if current_location is provided in the request
        if 'current_location' not in request.data:
            return Response({"error": "current_location is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Extract and validate the current_location field (must be 'latitude,longitude')
        location_data = request.data['current_location']
        try:
            latitude, longitude = map(float, location_data.split(','))
        except ValueError:
            return Response({"error": "Invalid location format. Expected 'latitude,longitude'."}, status=status.HTTP_400_BAD_REQUEST)

        # Update only the current_location field
        ride.update_location(latitude, longitude)

        # Return the updated ride data with the current_location
        return Response({
            'id': ride.id,
            'rider': ride.rider.id,
            'driver': ride.driver.id if ride.driver else None,
            'pickup_location': ride.pickup_location,
            'dropoff_location': ride.dropoff_location,
            'status': ride.status,
            'current_location': ride.current_location,  # Updated location
            'updated_at': ride.updated_at,
        }, status=status.HTTP_200_OK)
from .matching import *  
class RideAcceptView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            # Retrieve the ride object based on the provided primary key (pk)
            ride = Ride.objects.get(pk=pk)
        except Ride.DoesNotExist:
            # If the ride does not exist, return a 404 response
            return Response({"error": "Ride not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user is a driver by checking the 'is_driver' flag in the DriverProfile model
        if not hasattr(request.user, 'profile') or not request.user.profile.is_driver:
            # If the user is not a driver, return a 403 Forbidden response
            return Response({"error": "Only drivers can accept rides."}, status=status.HTTP_403_FORBIDDEN)

        # Check if the ride has already been accepted or if it's in a status where it cannot be accepted
        if ride.status not in ['requested']:
            return Response({"error": "This ride cannot be accepted. It is already in a different status."}, status=status.HTTP_400_BAD_REQUEST)

        # Assign the ride to the driver (the current authenticated user)
        ride.driver = request.user
        ride.status = 'accepted'  # Change the ride status to 'accepted'
        ride.save()

        # Serialize and return the updated ride data
        ride_serializer = RideSerializer(ride)
        return Response({"message": "Ride accepted successfully", "ride": ride_serializer.data}, status=status.HTTP_200_OK)