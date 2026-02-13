from .models import Guest
from django.shortcuts import render, redirect


def user_profile(request):
    context = {}
    if request.user.is_authenticated:
        context['user'] = request.user
    else:
        guest_name = request.session.get('guest_name', 'Guest')
        guest = Guest.objects.filter(name=guest_name).first()
        context['guest'] = guest

    return render(request, 'guests/user_profile.html', context)


def guest_register(request):
    if request.method == 'POST':
        guest_name = request.POST.get('guest_name')
        if guest_name:
            Guest.objects.create(name=guest_name)
            request.session['guest_name'] = guest_name
            return redirect('main')
    return render(request, 'guests/guest.html')