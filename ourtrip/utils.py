import jwt, random

from django.conf import settings
from django.http import JsonResponse

from users.models import User
from reservation.models import FlightReservation

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            token        = request.headers.get('Authorization', None)
            payload      = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
            user         = User.objects.get(id=payload['id'])
            request.user = user
        except jwt.exceptions.DecodeError:
            return JsonResponse({'message' : 'INVALID_TOKEN' }, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_USER'}, status=400)
        return func(self, request, *args, **kwargs)
    return wrapper


def create_new_code():
    not_unique = True
    while not_unique:
        rand_code = str(random.randint(10000000, 99999999))
        if not FlightReservation.objects.filter(code = rand_code):
            not_unique = False
    return rand_code