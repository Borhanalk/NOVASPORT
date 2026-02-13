from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Event
from locations.models import SportsFieldLocation, Favorite
from django.utils import timezone
from datetime import timedelta


class TestPagesViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )

        self.field = SportsFieldLocation.objects.create(
            name="Test Field",
            field_type="football",
            latitude=10.0,
            longitude=20.0,
            address="Test Address",
            average_rating=4.5
        )

        self.event = Event.objects.create(
            title="Test Event",
            description="Test Description",
            date=timezone.now() + timedelta(days=1),
            location="Test Location"
        )

        Favorite.objects.create(user=self.user, field=self.field)

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_main_view(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)

    def test_about_us_view(self):
        response = self.client.get(reverse('about_us'))
        self.assertEqual(response.status_code, 200)

    def test_popular_fields_view(self):
        response = self.client.get(reverse('popular_fields'))
        self.assertEqual(response.status_code, 200)

    def test_upcoming_events_view(self):
        response = self.client.get(reverse('upcoming_events'))
        self.assertEqual(response.status_code, 200)

    def test_favorites_list_view_authenticated(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse('favorites_list'))
        self.assertEqual(response.status_code, 200)

    def test_favorites_list_view_guest(self):
        response = self.client.get(reverse('favorites_list'))
        self.assertEqual(response.status_code, 302)  # الضيف يتم إعادة توجيهه
