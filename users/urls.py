from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from pages.views import favorites_list

urlpatterns = [
    path('sign-up/', views.sign_up, name='sign-up'),
    path('', views.user, name='user'),  # تعديل الرابط
    path('login/', auth_views.LoginView.as_view(
        template_name='users/login.html'), name='login'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('send-help-request/',
         views.handle_help_request, name='handle_help_request'),
    path('check_response/', views.check_response, name='check_response'),
    path('favorites/', favorites_list, name='favorites_list'),
]
