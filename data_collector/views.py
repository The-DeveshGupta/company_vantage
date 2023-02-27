from django.conf import settings
from django.http import JsonResponse
import requests
from django.views.decorators.csrf import csrf_exempt
from .models import (
    Ticker, StocksPrice
)
from .serializers import (
    TickerSerializer, StocksPriceSerializer
)


def healthcheck(request):
    return JsonResponse({'Status': 'API is connected!'})


@csrf_exempt
def search_symbols(request):
    if request.method == 'POST':
        keywords = request.POST.get('keywords')
        username = request.POST.get('username')
        if not keywords:
            return JsonResponse({'Status': 'Unprocessable Entity', 'data': None, "StatusCode": 422})
        try:
            ticker_obj = Ticker.objects.get(symbol=keywords)
            # add serializer
            return JsonResponse({'Status': 'Success', 'data': TickerSerializer(ticker_obj).data, "StatusCode": 200})
        except Ticker.DoesNotExist:
            url = f"{settings.STOCKS_DATA_PROVIDER}query?function=SYMBOL_SEARCH&keywords={keywords}" \
                  f"&apikey={settings.STOCKS_DATA_API_KEY}"
            response = requests.get(url)
            response_data = response.json()
        for result in reversed(response_data["bestMatches"]):
            ticker_obj = Ticker(symbol=result["1. symbol"], company_name=result["2. name"],
                                symbol_type=result["3. type"], region=result["4. region"],
                                market_open=result["5. marketOpen"], market_close=result["6. marketClose"],
                                timezone=result["7. timezone"], currency=result["8. currency"], created_by=username)
            ticker_obj.save()
        return JsonResponse({'Status': 'Success', 'data': TickerSerializer(ticker_obj).data,
                             "StatusCode": 200})


@csrf_exempt
def stocks_data(request):
    if request.method == 'POST':
        symbol = request.POST.get('symbol')
        username = request.POST.get('username')
        # check if user wants updated data
        if not symbol:
            return JsonResponse({'Status': 'Unprocessable Entity', 'data': None, "StatusCode": 422})
        function = request.POST.get('function', 'TIME_SERIES_DAILY_ADJUSTED')
        outputsize = request.POST.get('outputsize', 'Compact')

        try:
            stock_obj = StocksPrice.objects.get(symbol=symbol)
            # add serializer
            return JsonResponse({'Status': 'Success', 'data': StocksPriceSerializer(stock_obj).data, "StatusCode": 200})
        except StocksPrice.DoesNotExist:
            url = f"{settings.STOCKS_DATA_PROVIDER}query?function={function}&symbol={symbol}" \
                  f"&outputsize={str(outputsize)}&apikey={settings.STOCKS_DATA_API_KEY}"
            response = requests.get(url)
            response_data = response.json()
        result = response_data["Meta Data"]
        data = response_data["Time Series (Daily)"]
        stock_obj = StocksPrice(symbol=result["2. Symbol"], information=result["1. Information"],
                                last_refreshed=result["3. Last Refreshed"], timezone=result["5. Time Zone"],
                                data_size=result["4. Output Size"], data=data, created_by=username)
        stock_obj.save()
        return JsonResponse({'Status': 'Success', 'data': StocksPriceSerializer(stock_obj).data,
                             "StatusCode": 200})
    else:
        return JsonResponse({'Status': 'Wrong request method!', 'data': None, 'StatusCode': 405})
