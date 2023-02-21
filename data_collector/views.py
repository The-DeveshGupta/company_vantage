# Remove secrets
# Remove csrf_exempt

from django.conf import settings
from django.http import JsonResponse
import requests
from django.views.decorators.csrf import csrf_exempt


def healthcheck(request):
    return JsonResponse({'Status': 'API is connected!'})


@csrf_exempt
def stocks_data(request):
    if request.method == 'POST':
        symbol = request.POST.get('symbol')
        function = request.POST.get('function', 'TIME_SERIES_DAILY_ADJUSTED')
        outputsize = request.POST.get('outputsize', 'Compact')
        url = f"{settings.STOCKS_DATA_PROVIDER}query?function={function}&symbol={symbol}&outputsize={str(outputsize)}" \
              f"&apikey={settings.STOCKS_DATA_API_KEY}"
        response = requests.get(url)
        data = response.json()
        return JsonResponse({'Status': 'Success', 'data': data, "StatusCode": 200})
    else:
        return JsonResponse({'Status': 'Wrong request method!', 'data': None, 'StatusCode': 405})
