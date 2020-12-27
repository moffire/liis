from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from api.models import Workplace, Reservation


class ApiUrlPermissionsTest(TestCase):

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
		response = self.client.get(reverse('api:workplace_reservations', kwargs={'pk': 1}))
		self.assertEqual(response.status_code, 403)

		# authenticate user and resend request
		self.client.force_authenticate(user=self.user)
		response = self.client.get(reverse('api:workplace_reservations', kwargs={'pk': 1}))
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
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.data), 2)

	def test_reservation_list_by_workplace_id(self):
		response = self.client.get(reverse('api:workplace_reservations', kwargs={'pk': 1}))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.data), 3)

		response = self.client.get(reverse('api:workplace_reservations', kwargs={'pk': 2}))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.data), 1)

		# wrong workplace id
		response = self.client.get(reverse('api:workplace_reservations', kwargs={'pk': 500}))
		self.assertEqual(response.status_code, 200)
		self.assertListEqual(response.data, [])

	def test_unreserved_workplaces(self):

		response = self.client.get(reverse('api:base'), **{'QUERY_STRING': self.build_url('2020-01-01 15:00', '2020-01-01 18:00')})
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.data), 2)

		response = self.client.get(reverse('api:base'), **{'QUERY_STRING': self.build_url('2020-01-01 09:00', '2020-01-01 21:00')})
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.data), 0)

		response = self.client.get(reverse('api:base'), **{'QUERY_STRING': self.build_url('2020-01-01 09:30', '2020-01-01 17:30')})
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.data), 1)

		# no free workplaces in dates range
		response = self.client.get(reverse('api:base'), **{'QUERY_STRING': self.build_url('2020-01-01 09:00', '2020-01-01 21:00')})
		self.assertEqual(response.status_code, 200)
		self.assertListEqual(response.data, [])

		# wrong datetime format
		response = self.client.get(reverse('api:base'), **{'QUERY_STRING': self.build_url('2020-20-01 09:30', '2020-01-01 17:30')})
		self.assertEqual(response.status_code, 400)
		self.assertTrue(response.data['error'], msg='Введенные даты не валидны')

	@staticmethod
	def build_url(first_date, last_date):
		return 'datetime_from={}&datetime_to={}'.format(first_date, last_date)

class ApiModelsTest(TestCase):

	def setUp(self):
		self.workplace = Workplace.objects.create()
		self.reservation = Reservation.objects.create(workplace=self.workplace,
		                           reserved_from=datetime.strptime('2020-01-01 09:00', "%Y-%m-%d %H:%M"),
		                           reserved_to=datetime.strptime('2020-01-01 12:00', "%Y-%m-%d %H:%M"))

	def test_fail_reservation_creating(self):

		# dates intersections
		Reservation.objects.create(workplace=self.workplace,
		                           reserved_from=datetime.strptime('2020-01-01 10:00', "%Y-%m-%d %H:%M"),
		                           reserved_to=datetime.strptime('2020-01-01 14:00', "%Y-%m-%d %H:%M"))
		self.assertRaises(ValueError, msg='Введенные даты забронированы')

		# dates intersections
		Reservation.objects.create(workplace=self.workplace,
		                           reserved_from=datetime.strptime('2020-01-01 08:00', "%Y-%m-%d %H:%M"),
		                           reserved_to=datetime.strptime('2020-01-01 10:00', "%Y-%m-%d %H:%M"))
		self.assertRaises(ValueError, msg='Введенные даты забронированы')

		# start date and end date are equals
		Reservation.objects.create(workplace=self.workplace,
		                           reserved_from=datetime.strptime('2020-01-01 10:00', "%Y-%m-%d %H:%M"),
		                           reserved_to=datetime.strptime('2020-01-01 10:00', "%Y-%m-%d %H:%M"))
		self.assertRaises(ValueError, msg='Дата начала брони не может быть больше или равна дате окончания')

		# start date later than end date
		Reservation.objects.create(workplace=self.workplace,
		                           reserved_from=datetime.strptime('2020-01-01 12:00', "%Y-%m-%d %H:%M"),
		                           reserved_to=datetime.strptime('2020-01-01 10:00', "%Y-%m-%d %H:%M"))
		self.assertRaises(ValueError, msg='Дата начала брони не может быть больше или равна дате окончания')