import requests
from django.http import HttpResponse
from .access_token import pesapal_token
from django.conf import settings


def get_ipn_list(request):
    # Define environment ('sandbox' or 'live')
    APP_ENVIRONMENT = 'sandbox'  # You can change this to 'live' based on your needs

    if APP_ENVIRONMENT == 'sandbox':
        getIpnListUrl = "https://cybqa.pesapal.com/pesapalv3/api/URLSetup/GetIpnList"
    elif APP_ENVIRONMENT == 'live':
        getIpnListUrl = "https://pay.pesapal.com/v3/api/URLSetup/GetIpnList"
    else:
        return HttpResponse("Invalid APP_ENVIRONMENT", status=500)

    # Get the Pesapal token
    token = pesapal_token(request)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(getIpnListUrl, headers=headers)
        response.raise_for_status()  # Raise exception for bad status codes (4xx or 5xx)

        return HttpResponse(response.content, content_type="application/json")

    except requests.exceptions.RequestException as e:
        return HttpResponse(f"Error occurred: {str(e)}", status=500)
