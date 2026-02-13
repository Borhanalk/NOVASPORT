from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
import random
import string
from .models import HelpRequest


@login_required
def handle_help_request(request):
    if request.method == "POST":
        message = request.POST.get("help-message")  # جلب الرسالة من الطلب
        if message:  # التحقق من أن الحقل غير فارغ
            HelpRequest.objects.create(user=request.user, message=message)
            messages.success(
                request, "Your help request has been submitted successfully!")
            return redirect("about_us")
        else:
            messages.error(request, "The message field cannot be empty!")

    return render(request, "pages/about_us.html")


@login_required
def check_response(request):
    # جلب جميع الرسائل المرتبطة بالمستخدم الحالي
    responses = HelpRequest.objects.filter(user=request.user)

    # تمرير الرسائل إلى القالب لعرضها
    return render(request, "users/check_response.html", {
        "responses": responses})


def generate_random_password(length=12):
    """Generate a random password."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            new_password = generate_random_password()
            user.set_password(new_password)
            user.save()

            # Send email with the new password
            send_mail(
                'Password Reset Request',
                f'Your new password is: {new_password}',
                settings.EMAIL_HOST_USER,  # المرسل
                [email],  # المستلم
                fail_silently=False,
            )
            messages.success(
                request, 'A new password has been sent to your email.')
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'No user found with this email address.')
    return render(request, 'users/forgot_password.html')


def sign_up(request):
    if request.user.is_authenticated:
        return redirect('main')  # إعادة التوجيه للمستخدم المصادق عليه
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/sign_up.html', {'form': form})


@login_required
def user(request):
    return render(request, 'users/user.html')