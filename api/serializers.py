from rest_framework import serializers, fields
from api.models import Reservation, Workplace


class ReservationCreateSerializer(serializers.ModelSerializer):

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
		fields = ('workplace', 'reserved_from', 'reserved_to')


class ReservationFreeTimeListSerializer(serializers.ModelSerializer):
	workplace = serializers.IntegerField(source='pk')

	class Meta:
		model = Workplace
		fields = ('workplace',)