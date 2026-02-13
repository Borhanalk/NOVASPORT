from django.http import JsonResponse
from .models import SportsFieldLocation, Booking, Rating, Favorite
from math import radians, sin, cos, sqrt, atan2
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.shortcuts import redirect


def get_field_types(request):
    field_types = [choice[0] for choice in SportsFieldLocation.FIELD_TYPES]
    return JsonResponse(field_types, safe=False)


def get_field_names(request):
    fields = SportsFieldLocation.objects.all().values("id", "name")
    return JsonResponse(list(fields), safe=False)


def get_field_locations(request):
    fields = SportsFieldLocation.objects.all()

    data = [
        {
            "id": field.id,
            "name": field.name,
            "field_type": field.get_field_type_display(),
            "latitude": field.latitude,
            "longitude": field.longitude,
            "address": field.address,
            "description": field.description,
            "image": field.image.url if field.image else None,
            "detail_url": reverse('field_detail', args=[field.id]),
        }
        for field in fields
    ]
    return JsonResponse(data, safe=False)


def locations_json(request):
    field_type = request.GET.get('type', '')

    if field_type:
        locations = SportsFieldLocation.objects.filter(
            type=field_type).values()
    else:
        locations = SportsFieldLocation.objects.all().values()

    return JsonResponse(list(locations), safe=False)


def field_types(request):
    types = SportsFieldLocation.objects.values_list(
        'field_type', flat=True).distinct()
    return JsonResponse(list(types), safe=False)


def get_nearby_fields(request):
    user_latitude = float(request.GET.get('latitude', 0))
    user_longitude = float(request.GET.get('longitude', 0))
    max_distance_km = float(request.GET.get('max_distance', 10))

    def calculate_distance(lat1, lon1, lat2, lon2):
        R = 6371
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(
            radians(lat2)) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c

    fields = SportsFieldLocation.objects.all()

    nearby_fields = []
    for field in fields:
        distance = calculate_distance(
            user_latitude, user_longitude, field.latitude, field.longitude)
        if distance <= max_distance_km:
            nearby_fields.append({
                "id": field.id,
                "name": field.name,
                "field_type": field.get_field_type_display(),
                "latitude": field.latitude,
                "longitude": field.longitude,
                "address": field.address,
                "description": field.description,
                "image": field.image.url if field.image else None,
                "distance": round(distance, 2),
            })

    return JsonResponse(nearby_fields, safe=False)


def location_detail(request, id):
    field = get_object_or_404(SportsFieldLocation, id=id)
    return render(request, 'pages/field_detail.html', {
        'field': field
    })


@login_required
def field_detail(request, id):
    field = get_object_or_404(SportsFieldLocation, id=id)

    now = datetime.now()

    current_bookings = Booking.objects.filter(
        field=field,
        date=now.date(),
        time__lte=now.time()
    )

    is_available = True
    for booking in current_bookings:
        booking_end_time = (datetime.combine(booking.date, booking.time) +
                            timedelta(hours=booking.duration)).time()
        if now.time() <= booking_end_time:
            is_available = False
            break

    success_message = None
    error_message = None

    is_favorite = Favorite.objects.filter(
        user=request.user, field=field).exists()

    hours_range = range(1, 25)

    rating_range = range(1, 6)

    # معالجة الطلب POST
    if request.method == 'POST':
        if 'date' in request.POST and 'time' in request.POST and 'duration' in request.POST:# noqa
            date = request.POST.get('date')
            raw_time = request.POST.get('time')
            duration = request.POST.get('duration')

            time = raw_time.split(".")[0]

            try:
                overlapping_bookings = Booking.objects.filter(
                    field=field,
                    date=date,
                    time__lte=(datetime.strptime(time, '%H:%M') + timedelta(
                        hours=int(duration))).time(),
                )

                if not overlapping_bookings.exists():
                    Booking.objects.create(
                        field=field,
                        user=request.user,
                        date=date,
                        time=time,
                        duration=int(duration)
                    )
                    success_message = "You have successfully booked the field!"
                    return redirect('booking_confirmation', id=id)
                else:
                    error_message = "The field is unavailable for the selected time."# noqa
            except ValueError as e:
                error_message = f"Invalid time format: {e}"

        elif 'rating' in request.POST:
            rating_value = int(request.POST.get('rating', 0))
            if 1 <= rating_value <= 5:
                Rating.objects.update_or_create(
                    user=request.user,
                    field=field,
                    defaults={'rating': rating_value}
                )
                ratings = field.ratings.all()
                field.average_rating = sum(
                    r.rating for r in ratings) / ratings.count()
                field.save()
                success_message = "You have successfully rated this field!"
            else:
                error_message = "Invalid rating value. Please select a value between 1 and 5."# noqa

        elif 'favorite' in request.POST:
            favorite, created = Favorite.objects.get_or_create(
                user=request.user, field=field)
            if not created:
                favorite.delete()
                success_message = "The field has been removed from your favorites."# noqa
            else:
                success_message = "The field has been added to your favorites."

    return render(request, 'pages/field_detail.html', {
        'field': field,
        'is_available': is_available,
        'is_favorite': is_favorite,
        'success_message': success_message,
        'error_message': error_message,
        'hours_range': hours_range,
        'rating_range': rating_range
    })


def find_fields(request):
    fields = SportsFieldLocation.objects.all()

    field_type = request.GET.get('type', '')
    search_query = request.GET.get('search', '')

    if field_type:
        fields = fields.filter(field_type=field_type)
    if search_query:
        fields = fields.filter(name__icontains=search_query)

    return render(request, 'pages/find_fields.html', {
        'fields': fields,
        'field_type': field_type,
        'search_query': search_query,
    })


@login_required
def booking_confirmation(request, id):
    field = get_object_or_404(SportsFieldLocation, id=id)
    return render(request, 'pages/booking_confirmation.html',
                  {'field': field})
