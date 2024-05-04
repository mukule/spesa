from django.http import HttpResponseServerError
import base64
from .models import Blog, Category
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from main.models import *
from django.db.models import Count
from .forms import *
from securitiespesa.settings import consumer_key, consumer_secret
import requests
from base64 import b64encode
import datetime
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
shortcode = 174379
# Create your views here.


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
    return render(request, 'main/dashboard.html')


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
            # Pass the request object here
            response = initiate_payment(request)
            if response == "success":
                consult.save()
                return HttpResponse("Payment initiated successfully. Consult created.")
            else:
                return HttpResponseServerError("Failed to initiate payment. Consult not created.")
    else:
        form = ConsultForm()

    return render(request, 'main/create_consult.html', {'form': form, 'speciality': speciality})


def initiate_payment(request):
    if request.method == 'POST':
        # Get form data
        amount = request.POST.get('amount')
        phone_number = request.POST.get('phone_number')

        # Get an OAuth access token
        url = "https://sandbox.safaricom.co.ke/oauth/v1/generate"
        querystring = {"grant_type": "client_credentials"}

        credentials = f"{consumer_key}:{consumer_secret}"
        credentials_b64 = base64.b64encode(
            credentials.encode("ascii")).decode("ascii")

        headers = {"Authorization": f"Basic {credentials_b64}"}

        response = requests.request(
            "GET", url, headers=headers, params=querystring)

        response_json = response.json()
        access_token = response_json["access_token"]
        print(access_token)
        host = request.get_host()

        callback_url = 'http://soft01.kenyaweb.com:8081/tenders/payment_push'

        # Make M-Pesa payment request
        passkey = "KgJI3c0EoSYCuVdxUTyjGOL7P11CsxksY+BSY7+mwFObvBWGYa6wD4+vIkoypvv5zsohcG5QhrGc9sKBhfATO+wxqAatmoqGM0LXEzDy0Lp02Go1QUD8nw/PUPDH3M72BoFquaPy5Z/FaGg/GuVV8HPZuWGyO8SMXIXiHVZqJ/X7ul0dWvYt14SwFBh1LuZRttiY3L5IVsQzOQSoj2ta31s0ZHMPGiVyPT2hMwDPoYe686i/HOSp9eOjFimjbBd7G2l2P5MN3QnzcMQndouNh2hrWoooqduE3Ake/fvKy2XdcOwu8I54t1OVjHm4W1Fno3+ur7iy95uwgwX+89lZZQ=="
        password = base64.b64encode(
            f"{shortcode}{passkey}{timestamp}".encode("ascii")).decode("ascii")

        url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
        headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json'
        }

        payload = {
            'BusinessShortCode': shortcode,
            'Password': password,
            'Timestamp': timestamp,
            'TransactionType': 'CustomerPayBillOnline',
            'Amount': 1,
            'PartyA': '0704122212',
            'PartyB': 174379,
            'PhoneNumber': '0704122212',
            'CallBackURL': callback_url,
            'AccountReference': 'conference',
            'TransactionDesc': 'ticket',
        }

        response = requests.post(url, headers=headers, json=payload)

        print(response)

        # Check payment status and return appropriate response
        if response.status_code == 200:
            response_json = response.json()
            print(response_json)
            if response_json["ResponseCode"] == "0":
                return "success"  # Payment initiation successful
            else:
                return "failure"  # Payment initiation failed
        else:
            print(response)
            return "failure"  # Payment initiation failed due to HTTP error
    return render(request, 'main/tenders_detail.html')
