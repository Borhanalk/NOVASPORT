from django.urls import path
from . import views

urlpatterns = [
    path('get_field_types', views.get_field_types, name='get_field_types'),
    path('get_field_names', views.get_field_names, name='get_field_names'),
    path('get_field_locations', views.get_field_locations,
         name='get_field_locations'),
    path('locations_json', views.locations_json, name='locations_json'),
    path('field_types', views.get_field_types, name='field_types'),
    path('get_nearby_fields', views.get_nearby_fields,
         name='get_nearby_fields'),
    path('<int:id>/', views.location_detail, name='location_detail'),
    path('find_fields/', views.find_fields, name='find_fields'),
    path('locations/<int:id>/', views.field_detail, name='field_detail'),
    path('field/<int:id>/confirmation/', views.booking_confirmation,
         name='booking_confirmation'),
]