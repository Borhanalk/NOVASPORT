from django.contrib import admin
from .models import SportsFieldLocation
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('field', 'user', 'date', 'time', 'duration')


admin.site.register(SportsFieldLocation)
