from django.urls import path
from . import views

urlpatterns = [
    path('payment/<int:field_id>/', views.payment, name='payment'),
    path('payment/execute/', views.execute_payment, name='execute_payment'),
    path('payment/cancel/', views.payment_cancel, name='payment_cancel'),
]
