from rest_framework import generics
from datetime import timedelta, datetime
from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny

from api.serializers import ReservationCreateSerializer, ReservationListSerializer, ReservationFreeTimeListSerializer
from api.models import Reservation


class ReservationCreateView(generics.CreateAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = ReservationCreateSerializer


class ReservationListView(generics.ListAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = ReservationListSerializer

	def get_queryset(self):
		pk = self.kwargs.get('pk')
		return Reservation.objects.filter(workplace__pk=pk)


class ReservationFreeTimeListView(generics.ListAPIView):
	permission_classes = [AllowAny]
	serializer_class = ReservationFreeTimeListSerializer

	def get_queryset(self):
		start_date = self.request.query_params.get('datetime_from')
		end_date = self.request.query_params.get('datetime_to')
		if (start_date and end_date) is not None:
			try:
				parsed_start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M")
				parsed_end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M")
			except ValueError:
				raise ValidationError({'error': ['Введенные даты не валидны']})

			free_workplaces = Reservation.objects.exclude(Q(reserved_from__range = (parsed_start_date, parsed_end_date - timedelta(seconds=1))) |
		                                        Q(reserved_to__range = (parsed_start_date + timedelta(seconds=1), parsed_end_date)) |
		                                        Q(reserved_from__gte = parsed_start_date, reserved_to__lte=parsed_end_date))
			return free_workplaces.values('workplace_id').distinct()

		return Reservation.objects.values('workplace_id').distinct()
