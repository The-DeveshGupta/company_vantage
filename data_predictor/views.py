from django.http import JsonResponse


def healthcheck(request):
    return JsonResponse({'Status': 'API is connected'})
