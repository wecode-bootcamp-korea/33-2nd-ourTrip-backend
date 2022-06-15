from django.urls import path

from reservation.views import ReservationDetailView, ReservationListView

urlpatterns = [
    path('', ReservationListView.as_view()),
    path('/<int:reservation_id>', ReservationDetailView.as_view())
]
