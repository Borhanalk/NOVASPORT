from django.shortcuts import render, redirect
import paypalrestsdk
from django.conf import settings
from locations.models import SportsFieldLocation

paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})


def payment(request, field_id):
    field = SportsFieldLocation.objects.get(id=field_id)

    if request.method == 'POST':
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"  
            },
            "transactions": [{
                "amount": {
                    "total": str(field.price_per_hour),
                    "currency": "USD"
                },
                "description": f"Payment for booking field {field.name}"
            }],
            "redirect_urls": {
                "return_url": "http://localhost:8000/payment/execute/",
                "cancel_url": "http://localhost:8000/payment/cancel/"
            }
        })

        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    approval_url = link.href
                    return redirect(approval_url)
        else:
            print(payment.error)

    return render(request, 'payment/payment.html', {'field': field})


def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        return render(request, 'payments/payment_success.html')
    else:
        return render(request, 'payments/payment_failed.html')


def payment_cancel(request):
    return render(request, 'payments/payment_cancel.html')
