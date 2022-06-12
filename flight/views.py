from django.db.models import Q
from django.http import JsonResponse
from django.views import View

from flight.models import Flight

class FlightsListView(View):
    def get(self, request):
        date = request.GET.get('date', None)
        origin = request.GET.get('origin', None)
        destination = request.GET.get('destination', None)
        airlines = request.GET.getlist('airline', None)
        time_filters = request.GET.getlist('timefilter', ['0'])
        sort = request.GET.get('sort', 'low_price')

        time_filter_dic = {
            '0': [' 00:00:00', ' 23:59:59'],
            '1': [' 00:00:00', ' 06:00:00'],
            '2': [' 06:00:00', ' 12:00:00'],
            '3': [' 12:00:00', ' 18:00:00'],
            '4': [' 18:00:00', ' 23:59:59']
        }

        sort_dic = {
            'low_price'    : 'price',
            'fastest_first': 'departure_time',
            'fastest_last' : '-departure_time'
        }

        if not date:
            return JsonResponse({'message': 'NONE_DATE'}, status = 400)
        if not origin:    
            return JsonResponse({'message': 'NONE_ORIGIN'}, status = 400)
        if not destination:
            return JsonResponse({'message': 'NONE_DESTINATION'}, status=400)

        q = Q()
        for i in time_filters:
            from_time = date + time_filter_dic[i][0]
            to_time   = date + time_filter_dic[i][1]
            q        |= Q(departure_time__gte=from_time) & Q(departure_time__lte=to_time)
        
        q &= Q(route_id__origin_airport_id__code=origin)
        q &= Q(route_id__destination_airport_id__code=destination)

        if airlines:
            q_airline = Q()
            for air in airlines:
                q_airline |= Q(route_id__airline_id=air)
            q &= q_airline
        

        flights = Flight.objects.filter(q).order_by(sort_dic[sort])

        results = [
            {
                "flight_id"      : flight.id,
                "name"           : flight.route.airline.name,
                "flight_name"    : flight.route.flight_number,
                "price"          : format(flight.price,',d')+'원',
                "logo_url"       : flight.route.airline.img,
                "origin"         : flight.route.origin_airport.code,
                "kor_origin"     : flight.route.origin_airport.name,
                "destination"    : flight.route.destination_airport.code,
                "kor_destination": flight.route.destination_airport.name,
                "departure_time" : flight.departure_time.strftime('%H:%M'),
                "arrival_time"   : flight.arrival_time.strftime('%H:%M'),
                "duration"       : str(flight.arrival_time-flight.departure_time)[:-3]
            }
            for flight in flights
        ]

        return JsonResponse({'results': results}, status=200)

