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
	datetime_from = models.DateTimeField(verbose_name='Дата начала брони')
	datetime_to = models.DateTimeField(verbose_name='Дата окончания брони')

	def clean(self, *args, **kwargs):
		if self.datetime_from >= self.datetime_to:
			raise ValidationError('Дата начала брони не может быть больше или равна дате окончания')

		# checking date intersection with exists reservations
		workplace = Workplace.objects.get(pk=self.workplace.pk)
		intersections = workplace.reservations.filter(Q(datetime_from__range=[self.datetime_from, self.datetime_to - timedelta(seconds=1)]) |
		                                              Q(datetime_to__range=[self.datetime_from + timedelta(seconds=1), self.datetime_to]) |
		                                              Q(datetime_from__lt=self.datetime_from, datetime_to__gt=self.datetime_to))
		if intersections:
			raise ValidationError('Введенные даты забронированы')
