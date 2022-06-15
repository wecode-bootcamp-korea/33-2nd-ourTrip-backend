import jwt

from django.conf import settings
from django.test import TestCase, Client

from flight.models import Airline, Region, Airport, Route, Flight
from reservation.models import Passenger, FlightReservation
from users.models import User

class ReservationTest(TestCase):
    def setUp(self):
        User.objects.create(
            id = 1,
            kakao_id = 123456789,
            email = 'test_email',
            name = 'test_name'
        )
        Airline.objects.create(
            id = 1,
            name = '대한항공',
            img = 'test_img'
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
                name = '김포공항',
                code = 'GMP',
                region_id = 1
            ),
            Airport(
                id = 2,
                name = '제주공항',
                code = 'CJU',
                region_id = 2
            )
        ])
        Route.objects.create(            
            id = 1,
            flight_number = 'test_flight_number',
            airline_id = 1,
            origin_airport_id = 1,
            destination_airport_id = 2  
        )
        Flight.objects.create(
            id = 1,
            departure_time='2022-06-21 05:00:00',
            arrival_time='2022-06-21 06:00:00', 
            price=50000, 
            route_id= 1
        )
        FlightReservation.objects.create(
            id = 1,
            user_id =1,
            flight_id = 1,
            code = '01062266008'            
        )
        Passenger.objects.bulk_create([
            Passenger(
                id = 1,
                flightreservation_id =1,
                name = 'Byeonghwi Jeong',
                gender = '남성',
                birth = '1990-09-19',
                price=50000
            ),
            Passenger(
                id = 2,
                flightreservation_id =1,
                name = 'Hyeonmin Choi',
                gender = '남성',
                birth = '1996-09-19',
                price=50000
            ),                    
        ])
        self.token = jwt.encode({"id" : User.objects.get(id=1).id}, settings.SECRET_KEY, algorithm = settings.ALGORITHM)

    def tearDown(self):
        Passenger.objects.all().delete()
        FlightReservation.objects.all().delete()
        Flight.objects.all().delete()
        Route.objects.all().delete()
        Airport.objects.all().delete()
        Region.objects.all().delete()
        Airline.objects.all().delete()
        User.objects.all().delete()

    def test_success_reservationlist_get(self):
        client = Client()        
        headers = {'HTTP_Authorization': self.token}
        response = client.get('/reservations', **headers, content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                "results":[
                    {
                    'id': 1,
                    'code': '01062266008',
                    'airline' : '대한항공',
                    'kor_origin': '김포공항',
                    'kor_destination': '제주공항',
                    'logo_url': 'test_img',
                    'date': '2022-06-21'
                    }
                ]    
            }                
        )

    def test_success_reservationdetail_get(self):
        client = Client()
        headers = {'HTTP_Authorization': self.token}
        response = client.get('/reservations/1', **headers, content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                'results': {
                    'code': '01062266008', 
                    'airline': '대한항공', 
                    'kor_origin': '김포공항', 
                    'kor_destination': '제주공항', 
                    'origin': 'GMP', 
                    'destination': 'CJU', 
                    'logo_url': 'test_img', 
                    'date': '2022-06-21 Tuesday 05:00', 
                    'user_name': 'test_name', 
                    'user_email': 'test_email', 
                    'total_price': '100,000원', 
                    'passengers': [
                        {
                            'name': 'Byeonghwi Jeong', 
                            'gender': '남성', 
                            'birth': '1990-09-19', 
                            'price': 50000
                        }, 
                        {
                            'name': 'Hyeonmin Choi', 
                            'gender': '남성', 
                            'birth': '1996-09-19', 
                            'price': 50000
                        }
                    ]
                }
            }               
        )
