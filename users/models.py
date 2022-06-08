from django.db import models

from core.models import TimeStampModel

class User(TimeStampModel):
    kakao_id = models.CharField(max_length=100)
    name     = models.CharField(max_length=50)
    email    = models.CharField(max_length=200)
    point    = models.IntegerField(default=1000000)

    class Meta:
        db_table = 'users'

