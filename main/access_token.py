from django.shortcuts import render
from django.http import HttpResponse
import requests
import json
from securitiespesa.settings import pesapal_consumer_key, pesapal_consumer_secret


def pesapal_token(request):
    # Define environment ('sandbox' or 'live')
    APP_ENVIRONMENT = 'sandbox'  # You can change this to 'live' based on your needs

    if APP_ENVIRONMENT == 'sandbox':
        api_url = "https://cybqa.pesapal.com/pesapalv3/api/Auth/RequestToken"  # Sandbox URL
        consumer_key = pesapal_consumer_key
        consumer_secret = pesapal_consumer_secret
    elif APP_ENVIRONMENT == 'live':
        api_url = "https://pay.pesapal.com/v3/api/Auth/RequestToken"  # Live URL
        consumer_key = pesapal_consumer_key
        consumer_secret = pesapal_consumer_secret
    else:
        return HttpResponse("Invalid APP_ENVIRONMENT", status=500)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    data = {
        "consumer_key": consumer_key,
        "consumer_secret": consumer_secret
    }

    # Convert data to JSON string
    data_json = json.dumps(data)

    try:
        response = requests.post(api_url, data=data_json, headers=headers)
        response.raise_for_status()  # Raise exception for bad status codes (4xx or 5xx)

        data = response.json()
        token = data.get('token')

        if token:
            return token
        else:
            return HttpResponse("Failed to retrieve token", status=500)
            # Handle error scenario here if necessary

    except requests.exceptions.RequestException as e:
        return HttpResponse(f"Error occurred: {str(e)}", status=500)
        # Handle error scenario here if necessary
