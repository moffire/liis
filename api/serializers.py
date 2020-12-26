from rest_framework import serializers, fields
from api.models import Reservation


class ReservationCreateSerializer(serializers.ModelSerializer):

	datetime_from = fields.DateTimeField(input_formats=["%d.%m.%Y %H:%M"])
	datetime_to = fields.DateTimeField(input_formats=["%d.%m.%Y %H:%M"])

	def validate(self, attrs):
		instance = Reservation(**attrs)
		instance.clean()
		return attrs

	class Meta:
		model = Reservation
		fields = '__all__'


class ReservationListSerializer(serializers.ModelSerializer):

	class Meta:
		model = Reservation
		fields = ('workplace', 'datetime_from', 'datetime_to')