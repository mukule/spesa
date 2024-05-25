import time
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import os
from django.contrib import messages
from .invoice import *
from django.http import HttpResponseServerError
import base64
from .models import Blog, Category
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from main.models import *
from django.db.models import Count
from .forms import *
from securitiespesa.settings import consumer_key, consumer_secret, pass_key
import requests
from datetime import datetime
shortcode = 174379


def index(request):
    specialities = Speciality.objects.all()
    concerns = FinancialConcern.objects.all()
    abouts = About.objects.all()
    panel = Panel.objects.all()
    works = Works.objects.all()

    context = {
        'specialities': specialities,
        'concerns': concerns,
        'abouts': abouts,
        'panel': panel,
        'works': works
    }
    return render(request, 'main/index.html', context)


def choice(request):
    return render(request, 'main/choice.html')


def blogs(request):
    latest_blog = Blog.objects.latest('created_at')
    last_five_blogs = Blog.objects.order_by('-created_at')[:5]
    all_categories = Category.objects.annotate(num_blogs=Count('blog'))
    return render(request, 'main/blogs.html', {'blog': latest_blog, 'recent_blogs': last_five_blogs, 'categories': all_categories})


@login_required
def dashboard(request):
    user_consults = Consult.objects.filter(
        user=request.user).order_by('-id')[:5]

    return render(request, 'main/dashboard.html', {'user_consults': user_consults})


@login_required
def consultant(request):
    return render(request, 'main/consultant.html')


@login_required
def create_consult(request, speciality_id):
    speciality = get_object_or_404(Speciality, pk=speciality_id)

    if request.method == 'POST':
        form = ConsultForm(request.POST)
        if form.is_valid():
            consult = form.save(commit=False)
            consult.user = request.user
            consult.category = speciality.name
            consult.price = speciality.price
            consult.save()

            # Generate and send the invoice
            invoice_sent = send_invoice_email(
                request.user,
                speciality,
                consult.transaction_code,
                speciality.price,
                consult.description,
                consult.payment_confirmation
            )

            if invoice_sent:
                # Success message
                messages.success(
                    request, 'Consultation created successfully. Invoice sent to Your Email.')

            else:
                # Error message if invoice sending failed
                messages.error(
                    request, 'Failed to send invoice. Please contact support.')

            # Redirect back to the same page after creating consultation
            return redirect(request.path)
        else:
            # Error message if form is invalid
            messages.error(
                request, 'Failed to create consultation. Please check the form.')

    else:
        form = ConsultForm()

    return render(request, 'main/create_consult.html', {'form': form, 'speciality': speciality})


def format_phone_number(phone):
    """
    Convert phone number to the required format for M-PESA API.
    Assumes the phone number is in national format.
    """
    # Remove any non-digit characters
    phone = ''.join(filter(str.isdigit, phone))

    # Check if the number starts with a leading zero
    if phone.startswith('0'):
        # Remove the leading zero
        phone = phone[1:]

    # Add the country code
    phone = '254' + phone

    return phone


@login_required
def create_f_consult(request, concern_id):
    speciality = get_object_or_404(FinancialConcern, pk=concern_id)

    if request.method == 'POST':
        form = ConsultForm(request.POST)
        if form.is_valid():
            consult = form.save(commit=False)
            consult.user = request.user
            consult.category = speciality.name
            consult.price = speciality.price
            consult.payment_confirmation = False  # Pending
            consult.save()

            invoice_sent = send_invoice_email(
                request.user,
                speciality,
                consult.transaction_code,
                speciality.price,
                consult.description,
                consult.payment_confirmation
            )

            if invoice_sent:
                messages.success(
                    request, 'Consultation created successfully. Invoice sent to your email.')

                try:
                    phone = request.user.phone
                    user_phone = format_phone_number(phone)
                    payment_response = initiate_stk_push(
                        consult.price, user_phone, consult.category)

                    # Save the checkout request ID
                    consult.checkout_request_id = payment_response.get(
                        'CheckoutRequestID')
                    consult.save()

                    messages.success(
                        request, 'Payment initiated successfully. Please complete the payment on your phone.')

                    # Check payment status
                    payment_confirmed = check_payment_status(
                        consult.checkout_request_id)
                    if payment_confirmed:
                        messages.success(
                            request, 'Payment confirmed successfully.')
                    else:
                        messages.error(
                            request, 'Payment confirmation timed out or failed.')

                except Exception as e:
                    messages.error(
                        request, f'Failed to initiate payment: {str(e)}')

            else:
                # Error message if invoice sending failed
                messages.error(
                    request, 'Failed to send invoice. Please contact support.')

            # Redirect to main dashboard in all cases
            return redirect('main:dashboard')

        else:
            # Error message if form is invalid
            messages.error(
                request, 'Failed to create consultation. Please check the form.')

    else:
        form = ConsultForm()

    return render(request, 'main/create_consult.html', {'form': form, 'speciality': speciality})


def check_payment_status(checkout_request_id):
    timeout = 35  # seconds
    interval = 2  # seconds
    elapsed_time = 0

    while elapsed_time < timeout:
        try:
            consult = Consult.objects.get(
                checkout_request_id=checkout_request_id)
            if consult.payment_confirmation:
                return True
            else:
                time.sleep(interval)
                elapsed_time += interval
        except Consult.DoesNotExist:
            return False

    return False


@csrf_exempt
def mpesa_callback(request):
    if request.method == 'POST':
        try:
            # Parse the incoming JSON request
            data = json.loads(request.body.decode('utf-8'))

            # Extract relevant data
            body = data.get('Body', {})
            stk_callback = body.get('stkCallback', {})
            result_code = stk_callback.get('ResultCode')
            result_desc = stk_callback.get('ResultDesc')
            merchant_request_id = stk_callback.get('MerchantRequestID')
            checkout_request_id = stk_callback.get('CheckoutRequestID')
            callback_metadata = stk_callback.get(
                'CallbackMetadata', {}).get('Item', [])

            # Extract amount and phone number from callback metadata
            amount = None
            phone_number = None
            for item in callback_metadata:
                if item['Name'] == 'Amount':
                    amount = item['Value']
                elif item['Name'] == 'PhoneNumber':
                    phone_number = item['Value']

            # Update the Consultation object
            consultation = Consult.objects.get(
                checkout_request_id=checkout_request_id)
            if result_code == 0:
                # Successful transaction
                consultation.payment_confirmation = True
                consultation.transaction_code = merchant_request_id
                consultation.save()
                return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})
            else:
                # Failed transaction
                consultation.payment_confirmation = False
                consultation.save()
                return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})

        except Consult.DoesNotExist:
            # Handle the case where the transaction code does not match any Consultation
            return JsonResponse({"ResultCode": 1, "ResultDesc": "Consultation not found"})

        except Exception as e:
            # Handle any other exceptions
            return JsonResponse({"ResultCode": 1, "ResultDesc": str(e)})

    # If request method is not POST
    return JsonResponse({"ResultCode": 1, "ResultDesc": "Invalid request method"})


def get_token():
    api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    response = requests.get(api_url, auth=(consumer_key, consumer_secret))
    if response.status_code == 200:
        access_token = response.json()['access_token']
        return access_token
    else:
        raise Exception('Failed to get access token')

# Function to initiate M-PESA STK push


def generate_password(business_short_code, passkey):
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password_string = f"{business_short_code}{passkey}{timestamp}"
    password = base64.b64encode(password_string.encode()).decode('utf-8')
    return password


def initiate_stk_push(amount, phone, category):
    access_token = get_token()

    business_short_code = '174379'
    passkey = pass_key
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    print(timestamp)

    password = generate_password(business_short_code, passkey)

    api_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    payload = {
        "BusinessShortCode": business_short_code,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": float(amount),
        "PartyA": phone,
        "PartyB": 174379,
        "PhoneNumber": phone,
        "CallBackURL": "https://soft05.kenyaweb.com/mpesa_callback",
        "AccountReference": "SecuritiesPesa",
        "TransactionDesc": category,
    }
    response = requests.post(api_url, json=payload, headers=headers)
    if response.status_code == 200:
        print(response)
        return response.json()
    else:
        raise Exception(f'STK Push failed: {response.text}')


def success(request):
    return render(request, 'main/success.html')


def fail(request):
    return render(request, 'main/fail.html')
