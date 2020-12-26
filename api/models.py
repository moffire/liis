from datetime import timedelta
from django.db import models
from django.db.models import Q
from rest_framework.exceptions import ValidationError


class Workplace(models.Model):
	pass

	def __str__(self):
		return f'Рабочее место №{self.pk}'


class Reservation(models.Model):
	workplace = models.ForeignKey(Workplace, on_delete=models.CASCADE, related_name='reservations', verbose_name='Рабочее место')
	reserved_from = models.DateTimeField(verbose_name='Дата начала брони')
	reserved_to = models.DateTimeField(verbose_name='Дата окончания брони')

	def clean(self, *args, **kwargs):
		if self.reserved_from >= self.reserved_to:
			raise ValidationError({'error': ['Дата начала брони не может быть больше или равна дате окончания']})
		# checking date intersection with exists reservations
		workplace = Workplace.objects.get(pk=self.workplace.pk)
		intersections = workplace.reservations.filter(Q(reserved_from__range=[self.reserved_from, self.reserved_to - timedelta(seconds=1)]) |
		                                              Q(reserved_to__range=[self.reserved_from + timedelta(seconds=1), self.reserved_to]) |
		                                              Q(reserved_from__lt=self.reserved_from, reserved_to__gt=self.reserved_to))
		if intersections:
			raise ValidationError({'error': ['Введенные даты забронированы']})
