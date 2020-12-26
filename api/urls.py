from django.urls import path
from api.views import ReservationCreateView, ReservationListView, ReservationFreeTimeListView

app_name = 'api'

urlpatterns = [
	path('', ReservationFreeTimeListView.as_view(), name='base'),
	path('create/', ReservationCreateView.as_view(), name='create_reservation'),
	path('reservations/<int:pk>', ReservationListView.as_view(), name='reservations_list'),
]
