from django.urls import path
from api.views import ReservationCreateView, ReservationListView, ReservationFreeTimeListView

app_name = 'api'

urlpatterns = [
	path('create/', ReservationCreateView.as_view()),
	path('reservations/<int:pk>', ReservationListView.as_view()),
	path('reservations/', ReservationFreeTimeListView.as_view()),
]
