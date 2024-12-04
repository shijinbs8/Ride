from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('rides/', RideListView.as_view(), name='ride_list'),               
    path('rides/create/', RideCreateView.as_view(), name='ride_create'),   
    path('rides/<int:pk>/', RideDetailView.as_view(), name='ride_detail'), 
    path('rides/<int:pk>/status/', RideStatusUpdateView.as_view(), name='ride_status_update'),
    path('rides/<int:pk>/location/update/', RideLocationUpdateView.as_view(), name='ride_location_update'),
    path('rides/<int:pk>/accept/', RideAcceptView.as_view(), name='accept-ride'),




  
]