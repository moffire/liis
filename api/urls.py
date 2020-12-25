from django.urls import path
from api.views import ReservationCreateView, ReservationListView

app_name = 'api'

urlpatterns = [
	path('create/', ReservationCreateView.as_view()),
	path('reservations/<int:pk>', ReservationListView.as_view())
]
