from django.urls import path

from flight.views import FlightsListView

urlpatterns = [
    path('', FlightsListView.as_view())
]
