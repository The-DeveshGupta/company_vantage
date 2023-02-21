from django.http import HttpResponse, JsonResponse

def healthcheck(request):
    return JsonResponse({'Status': 'API is connected'})