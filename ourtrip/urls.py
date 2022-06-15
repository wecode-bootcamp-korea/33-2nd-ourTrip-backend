from django.urls import path, include

urlpatterns = [
    path('users', include('users.urls')),
    path('flights', include('flight.urls')),
    path('reservations', include('reservation.urls'))   
]
