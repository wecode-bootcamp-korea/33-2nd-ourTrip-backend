from django.http import JsonResponse
from django.views import View
from django.db.models import Sum

from ourtrip.utils import login_decorator
from reservation.models import FlightReservation

class ReservationListView(View):
    @login_decorator
    def get(self, request):
        user = request.user
        reservations = FlightReservation.objects.filter(user_id=user.id)
        
        results = [
            {
                "id"             : reservation.id,
                "code"           : reservation.code,
                "airline"        : reservation.flight.route.airline.name,
                "kor_origin"     : reservation.flight.route.origin_airport.name,
                "kor_destination": reservation.flight.route.destination_airport.name,
                "logo_url"       : reservation.flight.route.airline.img,
                "date"           : reservation.flight.departure_time.strftime('%Y-%m-%d')
            }
            for reservation in reservations
        ]

        return JsonResponse({'results': results}, status= 200)

class ReservationDetailView(View):
    @login_decorator
    def get(self, request, reservation_id):
        try:
            user            = request.user
            reservation     = FlightReservation.objects.get(id=reservation_id)
            passengers      = reservation.passenger_set.all()
            total_price     = format(passengers.aggregate(Sum('price'))['price__sum'],',d')+'원'
            passengers_info = [
                {
                    "name"  : passenger.name,
                    "gender": passenger.gender,
                    "birth" : passenger.birth.isoformat(),
                    "price" : passenger.price
                }
                for passenger in passengers
            ]   
            reservation_detail = {
                "code"           : reservation.code,
                "airline"        : reservation.flight.route.airline.name,
                "kor_origin"     : reservation.flight.route.origin_airport.name,
                "kor_destination": reservation.flight.route.destination_airport.name,
                "origin"         : reservation.flight.route.origin_airport.code,
                "destination"    : reservation.flight.route.destination_airport.code,
                "logo_url"       : reservation.flight.route.airline.img,
                "date"           : reservation.flight.departure_time.strftime('%Y-%m-%d %A %H:%M'),
                "user_name"      : user.name,
                "user_email"     : user.email,
                "total_price"    : total_price,
                "passengers"     : passengers_info
            }
            return JsonResponse({'results': reservation_detail}, status=200)
        except:
            return JsonResponse({'message': 'DOES_NOT_EXIST'}, status=200)


