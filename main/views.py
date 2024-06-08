from django.db.models import Sum
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
business_short_code = '174379'


def index(request):
    specialities = Speciality.objects.all()
    concerns = FinancialConcern.objects.all()
    abouts = About.objects.all()
    panel = Panel.objects.all()
    works = Works.objects.all()

    try:
        hero_instance = Hero.objects.get(pk=1)
    except Hero.DoesNotExist:
        hero_instance = None

    try:
        section1_instance = Section1.objects.get(pk=1)
    except Section1.DoesNotExist:
        section1_instance = None

    try:
        section2_instance = Section2.objects.get(pk=1)
    except Section2.DoesNotExist:
        section2_instance = None

    try:
        how_instance = How.objects.get(pk=1)
    except How.DoesNotExist:
        how_instance = None

    context = {
        'specialities': specialities,
        'concerns': concerns,
        'abouts': abouts,
        'panel': panel,
        'works': works,
        'hero': hero_instance,
        'section1': section1_instance,
        'section2': section2_instance,
        'how': how_instance,

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
    last_receipt = Consult.objects.filter(
        user=request.user,
        payment_confirmation=True
    ).order_by('-id').first()
    print(last_receipt)

    return render(request, 'main/dashboard.html', {'user_consults': user_consults, 'last_receipt': last_receipt})


@login_required
def consultant(request):
    if request.user.access_level == 2:  # Check if the logged-in user is a consultant
        # Retrieve commission instances for the user
        user_commissions = Commission.objects.filter(user=request.user)

        # Calculate total commission amount
        total_commission = user_commissions.aggregate(
            total=Sum('consult__commission'))['total']

        # Filter assigned consults for the user
        assigned_consults = Consult.objects.filter(handler=request.user)

        return render(request, 'main/consultant.html', {'tasks': assigned_consults, 'commissions': user_commissions, 'total_commission': total_commission})
    else:
        # Redirect or show an error message for users who are not consultants
        return render(request, 'main/consultant.html')


@login_required
def consult_detail(request, consult_id):
    consult = get_object_or_404(Consult, id=consult_id)
    responses = Response.objects.filter(consult=consult)
    accepted_responses = Response.objects.filter(
        consult=consult, accepted=True)
    user = request.user

    # Check if the logged-in user is the handler for the consult
    is_handler = user == consult.handler

    is_client = user.access_level == 3
    is_admin = user.access_level == 1 or user.is_superuser

    # Handling response update
    if request.method == 'POST':
        response_id = request.POST.get('response_id')
        response = get_object_or_404(Response, id=response_id)
        form = ClientResponseForm(request.POST, instance=response)
        if form.is_valid():
            form.save()
            return redirect('main:consult_detail', consult_id=consult_id)
    else:
        form = ClientResponseForm()

    return render(request, 'main/task_detail.html', {
        'consult': consult,
        'responses': responses,
        'is_handler': is_handler,
        'is_client': is_client,
        'accepted_responses': accepted_responses,
        'form': form,
        'is_admin': is_admin,
    })


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

            # Initiating payment
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
                    request, 'Payment initiated successfully.')
                return check_payment_status(request, consult.checkout_request_id)
            except Exception as e:
                messages.error(
                    request, 'Failed to initiate payment. Please try again.')

            # Sending email
            try:
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

            except Exception as e:
                pass  # Let the email fail silently

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

            # Initiating payment
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
                    request, 'Payment initiated successfully.')

                return check_payment_status(request, consult.checkout_request_id)
            except Exception as e:
                messages.error(
                    request, f'Failed to initiate payment. Please try again.')

            # Sending email
            try:
                send_invoice_email(
                    request.user,
                    speciality,
                    consult.transaction_code,
                    speciality.price,
                    consult.description,
                    consult.payment_confirmation
                )
            except Exception as e:
                pass  # Let the email fail silently

            messages.success(
                request, 'Request created successfully.')

            # Redirect to success page after completing all steps
            return redirect('success_page')

        else:
            messages.error(
                request, 'Failed to create Request. Please check the form and try again.')

    else:
        form = ConsultForm()

    return render(request, 'main/create_consult.html', {'form': form, 'speciality': speciality})


def check_payment_status(request, checkout_request_id):
    timeout = 20  # seconds
    interval = 2  # seconds
    elapsed_time = 0

    while elapsed_time < timeout:
        result = query_stk_push_status(checkout_request_id)
        result_code = result.get('ResultCode')

        if result_code == '0':
            try:
                consult = Consult.objects.get(
                    checkout_request_id=checkout_request_id)
                consult.payment_confirmation = True
                consult.transaction_code = result.get('MerchantRequestID')
                consult.save()
                messages.success(request, 'Payment confirmed successfully.')
                return redirect('main:dashboard')
            except Consult.DoesNotExist:
                messages.error(request, 'Consultation not found.')
                return redirect('main:dashboard')
        else:
            time.sleep(interval)
            elapsed_time += interval

    messages.error(request, 'Payment Confirmation')
    return redirect('main:dashboard')


@csrf_exempt
def mpesa_callback(request):
    if request.method == 'POST':
        try:
            callback_data = json.loads(request.body.decode('utf-8'))

            # Check the result code
            result_code = callback_data['Body']['stkCallback']['ResultCode']
            checkout_request_id = callback_data['Body']['stkCallback']['CheckoutRequestID']
            if result_code != 0:
                # If the result code is not 0, there was an error
                error_message = callback_data['Body']['stkCallback']['ResultDesc']
                response_data = {'ResultCode': result_code,
                                 'ResultDesc': error_message}

                # Update the Consult instance to indicate a failed transaction
                try:
                    consultation = Consult.objects.get(
                        checkout_request_id=checkout_request_id)
                    consultation.payment_confirmation = False
                    consultation.save()
                except Consult.DoesNotExist:
                    pass  # Log or handle the error appropriately

                return JsonResponse(response_data)

            # If the result code is 0, the transaction was completed
            callback_metadata = callback_data['Body']['stkCallback']['CallbackMetadata']
            amount = None
            phone_number = None
            for item in callback_metadata['Item']:
                if item['Name'] == 'Amount':
                    amount = item['Value']
                elif item['Name'] == 'PhoneNumber':
                    phone_number = item['Value']

            # Update the Consult instance to indicate a successful transaction
            try:
                consultation = Consult.objects.get(
                    checkout_request_id=checkout_request_id)
                consultation.payment_confirmation = True
                consultation.transaction_code = callback_data['Body']['stkCallback']['MerchantRequestID']
                consultation.save()
            except Consult.DoesNotExist:
                return JsonResponse({'ResultCode': 1, 'ResultDesc': 'Request not found'}, status=400)

            # Return a success response to the M-Pesa server
            response_data = {'ResultCode': 0, 'ResultDesc': 'Success'}
            return JsonResponse(response_data)

        except json.JSONDecodeError:
            return JsonResponse({'ResultCode': 1, 'ResultDesc': 'Invalid JSON'}, status=400)
        except KeyError as e:
            return JsonResponse({'ResultCode': 1, 'ResultDesc': f'Missing key: {str(e)}'}, status=400)

    return JsonResponse({'ResultCode': 1, 'ResultDesc': 'Invalid request method'}, status=405)


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


def query_stk_push_status(checkout_request_id):
    access_token = get_token()

    passkey = pass_key
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password = generate_password(business_short_code, passkey)

    api_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    payload = {
        "BusinessShortCode": business_short_code,
        "Password": password,
        "Timestamp": timestamp,
        "CheckoutRequestID": checkout_request_id,
    }

    response = requests.post(api_url, json=payload, headers=headers)

    try:
        response_json = response.json()
        print(f"Response JSON: {response_json}")
    except ValueError:
        print(f"Response Content (non-JSON): {response.content}")
        response_json = {}
    return response.json()


def toggle_task_acceptance(request, consult_id):
    consult = get_object_or_404(Consult, id=consult_id)

    # Toggle the task_accepted field
    consult.task_accepted = not consult.task_accepted
    consult.save()

    # Create Commission instance if task is accepted
    if consult.task_accepted:
        # Retrieve the logged-in user
        user = request.user

        # Create Commission instance
        commission = Commission.objects.create(user=user, consult=consult)

    return redirect('main:consultant')


@login_required
def create_response(request, consult_id):
    consult = get_object_or_404(Consult, id=consult_id)

    if request.method == 'POST':
        form = ResponseForm(request.POST, request.FILES)
        if form.is_valid():
            response = form.save(commit=False)
            response.consult = consult
            response.save()
            messages.success(request, 'Response successfully created!')
            return redirect('main:task_detail', consult_id=consult_id)
        else:
            messages.error(
                request, 'Failed to create response. Please correct the errors in the form.')
    else:
        form = ResponseForm()

    return render(request, 'main/create_response.html', {'form': form, 'consult': consult})


@login_required
def response_detail(request, response_id):
    response = get_object_or_404(Response, id=response_id)

    user = request.user
    is_admin = user.is_superuser or (
        user.access_level == 1 if hasattr(user, 'access_level') else False)
    return render(request, 'main/response_detail.html', {'response': response, 'is_admin': is_admin})


@login_required
def update_response(request, response_id):
    response = get_object_or_404(Response, id=response_id)
    consult_id = response.consult_id

    if request.method == 'POST':
        form = ClientResponseForm(request.POST, instance=response)
        if form.is_valid():
            form.save()
            return redirect('main:consult_detail', consult_id=consult_id)
    else:
        form = ClientResponseForm(instance=response)

    return render(request, 'main/task_detail.html', {'form': form, 'response': response})
