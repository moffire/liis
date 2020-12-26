from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from api.models import Workplace, Reservation


class ApiURLTest(TestCase):

	def setUp(self):
		self.client = APIClient()
		self.user = User.objects.create_user(username='user', password='password123')

	def test_base_url_access(self):
		response = self.client.get(reverse('api:base'))
		self.assertEqual(response.status_code, 200)

	def test_create_url_access(self):
		response = self.client.get(reverse('api:create_reservation'))
		self.assertEqual(response.status_code, 403)

		# authenticate user and resend request
		self.client.force_authenticate(user=self.user)
		response = self.client.get(reverse('api:create_reservation'))
		self.assertEqual(response.status_code, 405)

	def test_reservations_url_access(self):
		response = self.client.get(reverse('api:reservations_list', kwargs={'pk': 1}))
		self.assertEqual(response.status_code, 403)

		# authenticate user and resend request
		self.client.force_authenticate(user=self.user)
		response = self.client.get(reverse('api:reservations_list', kwargs={'pk': 1}))
		self.assertEqual(response.status_code, 200)


class ApiContentTest(TestCase):

	def setUp(self):
		self.client = APIClient()
		self.user = User.objects.create_user(username='user', password='password123')
		self.client.force_authenticate(user=self.user)

		for _ in range(2):
			Workplace.objects.create()

		Reservation.objects.create(workplace_id=1,
		                           reserved_from=datetime.strptime('2020-01-01 09:00', "%Y-%m-%d %H:%M"),
		                           reserved_to=datetime.strptime('2020-01-01 12:00', "%Y-%m-%d %H:%M"))

		Reservation.objects.create(workplace_id=1,
		                           reserved_from=datetime.strptime('2020-01-01 12:00', "%Y-%m-%d %H:%M"),
		                           reserved_to=datetime.strptime('2020-01-01 15:00', "%Y-%m-%d %H:%M"))

		Reservation.objects.create(workplace_id=1,
		                           reserved_from=datetime.strptime('2020-01-01 18:00', "%Y-%m-%d %H:%M"),
		                           reserved_to=datetime.strptime('2020-01-01 21:00', "%Y-%m-%d %H:%M"))

		Reservation.objects.create(workplace_id=2,
		                           reserved_from=datetime.strptime('2020-01-01 18:00', "%Y-%m-%d %H:%M"),
		                           reserved_to=datetime.strptime('2020-01-01 21:00', "%Y-%m-%d %H:%M"))

	def test_base_url_content(self):
		response = self.client.get(reverse('api:base'))
		self.assertEqual(len(response.data), 2)

	def test_reservation_list_by_workplace_id(self):
		response = self.client.get(reverse('api:reservations_list', kwargs={'pk': 1}))
		self.assertEqual(len(response.data), 3)

		response = self.client.get(reverse('api:reservations_list', kwargs={'pk': 2}))
		self.assertEqual(len(response.data), 1)

	def test_unreserved_workplaces(self):

		response = self.client.get(reverse('api:base'), **{'QUERY_STRING': self.build_url('2020-01-01 15:00', '2020-01-01 18:00')})
		self.assertEqual(len(response.data), 2)

		response = self.client.get(reverse('api:base'), **{'QUERY_STRING': self.build_url('2020-01-01 09:00', '2020-01-01 21:00')})
		self.assertEqual(len(response.data), 0)

		response = self.client.get(reverse('api:base'), **{'QUERY_STRING': self.build_url('2020-01-01 09:30', '2020-01-01 17:30')})
		self.assertEqual(len(response.data), 1)

	@staticmethod
	def build_url(first_date, last_date):
		return 'datetime_from={}&datetime_to={}'.format(first_date, last_date)