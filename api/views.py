from rest_framework import generics
from datetime import timedelta, datetime
from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny

from api.serializers import ReservationCreateSerializer, ReservationListSerializer, ReservationFreeTimeListSerializer
from api.models import Reservation, Workplace

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

			# check intersection with exists reservations
			reserved_workplaces = Reservation.objects.filter(Q(reserved_from__range=(parsed_start_date, parsed_end_date - timedelta(seconds=1))) |
			                                                 Q(reserved_to__range=(parsed_start_date + timedelta(seconds=1), parsed_end_date)) |
			                                                 Q(reserved_from__gte=parsed_start_date, reserved_to__lte=parsed_end_date) |
			                                                 Q(reserved_from__lte=parsed_start_date, reserved_to__gte=parsed_end_date))\
				.values_list('workplace_id', flat=True)\
				.distinct()
			return Workplace.objects.exclude(pk__in=reserved_workplaces)

		return Workplace.objects.all()


class ReservationCreateView(generics.CreateAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = ReservationCreateSerializer


class ReservationListView(generics.ListAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = ReservationListSerializer

	def get_queryset(self):
		pk = self.kwargs.get('pk')
		if pk:
			return Reservation.objects.filter(workplace__pk=pk)
		else:
			return Reservation.objects.all()