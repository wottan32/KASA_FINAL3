from django.http import HttpResponse
from django.shortcuts import render

from .forms import CustomerInfoForm


def customer_info(request):
    if request.method == 'POST':
        customer_form = CustomerInfoForm(request.method)
        if customer_form.is_valid() and customer_form.cleaned_data:
            customer_form.save()
            return render(request, 'paystack/payment.html', {'email': customer_form.email})
        else:
            return HttpResponse('Invalid input try again!!!')
    else:
        customer_form = CustomerInfoForm()
    return render(request, 'paystack/customer_info.html', {'customer_form': customer_form})
