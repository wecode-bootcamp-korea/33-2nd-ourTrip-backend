from django.db import models

from core.models import TimeStampModel

class FlightReservation(TimeStampModel):
    user   = models.ForeignKey('users.User', on_delete=models.CASCADE)
    flight = models.ForeignKey('flight.Flight', on_delete=models.CASCADE)
    code   = models.CharField(unique=True, max_length=50)

    class Meta:
        db_table = 'flight_reservations'

class Passenger(models.Model):
    flightreservation = models.ForeignKey('reservation.FlightReservation', on_delete=models.CASCADE)
    name              = models.CharField(max_length=50)
    gender            = models.CharField(max_length=50)
    birth             = models.DateField()
    price             = models.IntegerField()

    class Meta:
        db_table = 'passengers'

