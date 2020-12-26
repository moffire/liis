from rest_framework import serializers, fields
from api.models import Reservation


class ReservationCreateSerializer(serializers.ModelSerializer):

	datetime_from = fields.DateTimeField()
	datetime_to = fields.DateTimeField()

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


class ReservationFreeTimeListSerializer(serializers.ModelSerializer):

	class Meta:
		model = Reservation
		fields = ('workplace',)