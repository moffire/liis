from rest_framework import serializers, fields
from api.models import Reservation


class ReservationCreateSerializer(serializers.ModelSerializer):

	def validate(self, attrs):
		instance = Reservation(**attrs)
		instance.clean()
		return attrs

	class Meta:
		model = Reservation
		fields = '__all__'


class ReservationListSerializer(serializers.ModelSerializer):

	datetime_from = fields.DateField(input_formats=["%d.%m.%Y %H:%M"])
	datetime_to = fields.DateField(input_formats=["%d.%m.%Y %H:%M"])

	class Meta:
		model = Reservation
		fields = ('workplace', 'datetime_from', 'datetime_to')