from django.db import models

class Airline(models.Model):
    name = models.CharField(max_length=50)
    img = models.CharField(max_length=250)

    class Meta:
        db_table = 'airlines'

class Region(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'regions'

class Airport(models.Model):
    region = models.ForeignKey("flight.Region", on_delete=models.CASCADE)
    name   = models.CharField(max_length=100)
    code   = models.CharField(max_length=50)

    class Meta:
        db_table = 'airports'

class Route(models.Model):
    flight_number       = models.CharField(max_length=50)
    airline             = models.ForeignKey("flight.Airline", on_delete=models.CASCADE)
    origin_airport      = models.ForeignKey("flight.Airport", on_delete=models.CASCADE, related_name='origin')
    destination_airport = models.ForeignKey("flight.Airport", on_delete=models.CASCADE, related_name='destination')

    class Meta:
        db_table = 'routes'

class Flight(models.Model):
    departure_time = models.DateTimeField()
    arrival_time   = models.DateTimeField()
    price          = models.IntegerField()
    route          = models.ForeignKey("flight.Route", on_delete=models.CASCADE)

    class Meta:
        db_table = 'flights'


