from django.shortcuts import render, redirect
from django.contrib.auth import logout
from locations.models import SportsFieldLocation
from .models import Event
from locations.models import Favorite
from django.contrib.auth.decorators import login_required
from django.utils import timezone


@login_required
def favorites_list(request):
    favorite_fields = Favorite.objects.filter(
        user=request.user).select_related('field')

    context = {
        'favorite_fields': [fav.field for fav in favorite_fields],
    }
    return render(request, 'pages/favorites.html', context)


def user_logout(request):
    logout(request)
    return redirect('home')


def home(request):
    return render(request, 'pages/home.html')


def main(request):
    return render(request, 'pages/main.html')


def About_us(request):
    return render(request, 'pages/about_us.html')


def popular_fields(request):
    fields = SportsFieldLocation.objects.order_by('-average_rating')[:10]
    return render(request, 'pages/popular_fields.html', {'fields': fields})


def upcoming_events(request):
    events = Event.objects.filter(date__gte=timezone.now()).order_by('date')
    return render(request, 'pages/upcoming_events.html', {'events': events})