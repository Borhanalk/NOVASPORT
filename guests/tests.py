from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from guests.models import Guest


class TestGuestViews(TestCase):
    def setUp(self):
        """إعداد البيانات الأساسية للاختبارات."""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.guest_register_url = reverse("save_guest")
        self.user_profile_url = reverse("user_profile")

    # اختبار دالة guest_register
    def test_guest_register_valid(self):
        """Testing the `guest_register` view with a valid guest name."""
        response = self.client.post(self.guest_register_url, {
            "guest_name": "Guest123"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Guest.objects.filter(name="Guest123").exists())
        self.assertEqual(self.client.session["guest_name"], "Guest123")

    def test_guest_register_empty_name(self):
        """Testing the `guest_register` view with an empty guest name."""
        response = self.client.post(self.guest_register_url, {
            "guest_name": ""})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Guest.objects.exists())  # لا يتم إنشاء ضيف

    # اختبار دالة user_profile
    def test_user_profile_authenticated_user(self):
        """Testing the `user_profile` view for an authenticated user."""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.user_profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testuser")

    def test_user_profile_guest_user(self):
        """Testing the `user_profile` view for a guest user."""
        guest = Guest.objects.create(name="Guest123") # noqa
        session = self.client.session
        session["guest_name"] = "Guest123"
        session.save()

        response = self.client.get(self.user_profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Guest123")
