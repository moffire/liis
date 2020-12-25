from rest_framework import generics
from api.serializers import ReservationCreateSerializer, ReservationListSerializer
from api.models import Workplace, Reservation


class ReservationCreateView(generics.CreateAPIView):
	serializer_class = ReservationCreateSerializer


class ReservationListView(generics.ListAPIView):
	serializer_class = ReservationListSerializer


	def get_queryset(self):
		pk = self.kwargs.get('pk')
		return Reservation.objects.filter(workplace__pk = pk)