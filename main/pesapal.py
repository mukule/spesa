import requests
from django.http import HttpResponse
import json
from django.conf import settings
import random
from .access_token import pesapal_token


def submit_pesapal_order(request):
    # Generate a random merchant reference (assuming similar to PHP's rand function)
    print("we are here")
    merchantreference = random.randint(1, 1000000000000000000)

    phone = "0704122212"
    amount = 10.00
    callbackurl = "https://12eb-41-81-142-80.ngrok-free.app/pesapal/response-page.php"
    branch = "UMESKIA SOFTWARES"
    first_name = "Alvin"
    middle_name = "Odari"
    last_name = "Kiveu"
    email_address = "alvo967@gmail.com"

    # Define environment ('sandbox' or 'live')
    APP_ENVIRONMENT = 'sandbox'  # You can change this to 'live' based on your needs

    token = pesapal_token(request)

    print(token)

    if APP_ENVIRONMENT == 'sandbox':
        submitOrderUrl = "https://cybqa.pesapal.com/pesapalv3/api/Transactions/SubmitOrderRequest"
    elif APP_ENVIRONMENT == 'live':
        submitOrderUrl = "https://pay.pesapal.com/v3/api/Transactions/SubmitOrderRequest"
    else:
        return HttpResponse("Invalid APP_ENVIRONMENT", status=500)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    print(headers)

    # Request payload
    data = {
        "id": str(merchantreference),
        "currency": "KES",
        "amount": amount,
        "description": "Payment description goes here",
        "callback_url": callbackurl,
        "branch": branch,
        "billing_address": {
            "email_address": email_address,
            "phone_number": phone,
            "country_code": "KE",
            "first_name": first_name,
            "middle_name": middle_name,
            "last_name": last_name,
            "line_1": "Pesapal Limited",
            "line_2": "",
            "city": "",
            "state": "",
            "postal_code": "",
            "zip_code": ""
        }
    }

    try:
        response = requests.post(submitOrderUrl, json=data, headers=headers)
        print(response)
        response.raise_for_status()  # Raise exception for bad status codes (4xx or 5xx)

        response_data = response.json()
        print(response_data)
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    except requests.exceptions.RequestException as e:
        return HttpResponse(f"Error occurred: {str(e)}", status=500)
