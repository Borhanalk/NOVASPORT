from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from users.models import HelpRequest


class TestUserViews(TestCase):

    def setUp(self):
        """إعداد البيانات الأساسية للاختبارات."""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="testuser@example.com"
        )
        self.help_request_url = reverse("handle_help_request")
        self.check_response_url = reverse("check_response")
        self.forgot_password_url = reverse("forgot_password")
        self.sign_up_url = reverse("sign-up")
        self.user_url = reverse("user")

    def test_handle_help_request_valid(self):
        """اختبار دالة handle_help_request مع رسالة صالحة."""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(self.help_request_url, {
            "help-message": "I need help with booking!"
        })
        self.assertEqual(response.status_code, 302)  # إعادة التوجيه
        self.assertTrue(
            HelpRequest.objects.filter(
                user=self.user, message="I need help with booking!"
            ).exists()
        )

    def test_handle_help_request_empty_message(self):
        """اختبار دالة handle_help_request مع رسالة فارغة."""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            self.help_request_url, {"help-message": ""})
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any(msg.message == "The message field cannot be empty!" for msg in messages)# noqa
        )

    def test_check_response(self):
        """اختبار دالة check_response للمستخدمين المصادق عليهم."""
        HelpRequest.objects.create(user=self.user, message="Test help request")
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.check_response_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test help request")

    def test_forgot_password_valid_email(self):
        """اختبار دالة forgot_password مع بريد إلكتروني صالح."""
        response = self.client.post(self.forgot_password_url, {
            "email": "testuser@example.com"
        })
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any(msg.message == "A new password has been sent to your email." for msg in messages)# noqa
        )

    def test_forgot_password_invalid_email(self):
        """اختبار دالة forgot_password مع بريد إلكتروني غير صالح."""
        response = self.client.post(self.forgot_password_url, {
            "email": "invalid@example.com"
        })
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any(msg.message == "No user found with this email address." for msg in messages)# noqa
        )

    def test_sign_up_valid(self):
        """اختبار دالة sign_up مع بيانات صالحة."""
        response = self.client.post(self.sign_up_url, {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "securepassword123",
            "password2": "securepassword123",
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main'))
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_sign_up_invalid_passwords(self):
        """اختبار دالة sign_up مع كلمات مرور غير متطابقة."""
        response = self.client.post(self.sign_up_url, {
            "username": "newuser",
            "password1": "securepassword123",
            "password2": "wrongpassword",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The two password fields didn’t match.")

    def test_sign_up_existing_user(self):
        """اختبار دالة sign_up مع اسم مستخدم موجود بالفعل."""
        response = self.client.post(self.sign_up_url, {
            "username": "testuser",
            "password1": "securepassword123",
            "password2": "securepassword123",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "A user with that username already exists.")

    def test_sign_up_weak_password(self):
        """اختبار دالة sign_up مع كلمة مرور ضعيفة."""
        response = self.client.post(self.sign_up_url, {
            "username": "newuser",
            "password1": "123",
            "password2": "123",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This password is too short.")

    def test_sign_up_missing_fields(self):
        """اختبار دالة sign_up مع حقول مفقودة."""
        response = self.client.post(self.sign_up_url, {
            "username": "",
            "password1": "securepassword123",
            "password2": "securepassword123",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")

    def test_sign_up_authenticated_user(self):
        """اختبار دالة sign_up لمستخدم مصادق عليه بالفعل."""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.sign_up_url)
        self.assertRedirects(response, reverse('main'))

    def test_user_view(self):
        """اختبار دالة user للمستخدمين المصادق عليهم."""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.user_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome, testuser")
