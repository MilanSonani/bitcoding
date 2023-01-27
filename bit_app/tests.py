from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import Calendar, CustomUser


class CalendarViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword', email='testemail@yopmail.com', date_of_birth='2006-02-06', primary_contact_number='+919876543210')
        self.calendar = Calendar.objects.create(user=self.user, title='test meeting', start_time='2022-01-01T10:00:00Z', end_time='2022-01-01T11:00:00Z', meeting_ends_on='2022-04-01', recurrence='daily')
        self.data = {'user': self.user.id, 'title': 'test meeting', 'start_time': '2022-01-01T11:00:00Z', 'end_time': '2022-01-01T12:00:00Z', 'meeting_ends_on': '2022-04-01', 'recurrence': 'daily'}
        self.url = reverse('create-meeting')

    def test_post_calendar(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Calendar.objects.count(), 1)

    # def test_put_calendar(self):
    #     response = self.client.put(reverse('update-meeting', kwargs={'pk': self.calendar.id}), self.data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(Calendar.objects.count(), 1)
        # self.assertEqual(Calendar.objects.get(id=self.calendar.id).user.id, 'testuser')
        # self.assertEqual(Calendar.objects.get(id=self.calendar.id).start_time, '2022-01-01T11:00:00Z', '2022-04-01')

    def test_delete_calendar(self):
        response = self.client.delete(reverse('delete-meeting', kwargs={'pk': self.calendar.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Calendar.objects.count(), 0)
