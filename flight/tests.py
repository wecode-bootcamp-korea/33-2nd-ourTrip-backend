from django.test import TestCase, Client

from flight.models import Airline, Region, Airport, Route, Flight

class FlightsListTest(TestCase):
    def setUp(self):
        Airline.objects.create(
            id = 1,
            name = '대한항공',
            img = 'https://img.koreanair'
        )
        Region.objects.bulk_create([
            Region(
                id=1,
                name = '서울'
            ),
            Region(
                id=2,
                name = '제주'
            )
        ])
        Airport.objects.bulk_create([
            Airport(
                id = 1,
                name = '인천공항',
                code = 'ICN',
                region_id = 1
            ),
            Airport(
                id = 2,
                name = '김포공항',
                code = 'GMP',
                region_id = 1
            ),
            Airport(
                id =3,
                name = '제주공항',
                code = 'CJU',
                region_id = 2
            )
        ])
        Route.objects.create(            
            id = 1,
            flight_number = 'KE6226',
            airline_id = 1,
            origin_airport_id = 2,
            destination_airport_id = 3  
        )

        Flight.objects.bulk_create([
            Flight(
                id = 1,
                departure_time='2022-06-21 05:00:00',
                arrival_time='2022-06-21 06:00:00', 
                price=59000, 
                route_id= 1
            ),
            Flight(
                id = 2,
                departure_time='2022-06-21 09:00:00',
                arrival_time='2022-06-21 10:00:00', 
                price=58000, 
                route_id= 1
            ),
            Flight(
                id = 3,
                departure_time='2022-06-21 13:00:00',
                arrival_time='2022-06-21 14:00:00', 
                price=57000, 
                route_id= 1
            ),
            Flight(
                id = 4,
                departure_time='2022-06-21 18:00:00',
                arrival_time='2022-06-21 19:00:00', 
                price=56000, 
                route_id= 1
            ),
            Flight(
                id = 5,
                departure_time='2022-06-21 20:00:00',
                arrival_time='2022-06-21 21:00:00', 
                price=55000, 
                route_id= 1
            ),
        ])
        
    def tearDown(self):
        Flight.objects.all().delete()
        Route.objects.all().delete()
        Airline.objects.all().delete()
        Airport.objects.all().delete()
        Region.objects.all().delete()

    def test_success_flightslist_get(self):
        self.maxDiff = None
        client = Client()
        response = client.get('/flights?date=2022-06-21&origin=GMP&destination=CJU&timefilter=1&timefilter=4&airline=1&sort=fastest_last')       
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                "results": [
                    {
                        "flight_id": 5,
                        "name": "대한항공",
                        "flight_name": "KE6226",
                        "price": "55,000원",
                        "logo_url": "https://img.koreanair",
                        "origin": "GMP",
                        "kor_origin": "김포공항",
                        "destination": "CJU",
                        "kor_destination": "제주공항",
                        "departure_time": "20:00",
                        "arrival_time": "21:00",
                        "duration": "1:00"
                    },
                    {
                        "flight_id": 4,
                        "name": "대한항공",
                        "flight_name": "KE6226",
                        "price": "56,000원",
                        "logo_url": "https://img.koreanair",
                        "origin": "GMP",
                        "kor_origin": "김포공항",
                        "destination": "CJU",
                        "kor_destination": "제주공항",
                        "departure_time": "18:00",
                        "arrival_time": "19:00",
                        "duration": "1:00"
                    },
                    {
                        "flight_id": 1,
                        "name": "대한항공",
                        "flight_name": "KE6226",
                        "price": "59,000원",
                        "logo_url": "https://img.koreanair",
                        "origin": "GMP",
                        "kor_origin": "김포공항",
                        "destination": "CJU",
                        "kor_destination": "제주공항",
                        "departure_time": "05:00",
                        "arrival_time": "06:00",
                        "duration": "1:00"
                    }                    
                ]
            }
        )

    def test_fail_flightslist_nodate_get(self):
        client = Client()
        response = client.get('/flights?origin=GMP&destination=CJU&timefilter=1&timefilter=4&airline=1&sort=fastest_last')

        self.assertEqual(response.json(), {'message': 'NONE_DATE'})
        self.assertEqual(response.status_code, 400)
        
    def test_fail_flightslist_noorigin_get(self):
        client = Client()
        response = client.get('/flights?date=2022-06-21&destination=CJU&timefilter=1&timefilter=4&airline=1&sort=fastest_last')

        self.assertEqual(response.json(), {'message': 'NONE_ORIGIN'})
        self.assertEqual(response.status_code, 400)

    def test_fail_flightslist_nodestination_get(self):
        client = Client()
        response = client.get('/flights?date=2022-06-21&origin=GMP&timefilter=1&timefilter=4&airline=1&sort=fastest_last')

        self.assertEqual(response.json(), {'message': 'NONE_DESTINATION'})
        self.assertEqual(response.status_code, 400)