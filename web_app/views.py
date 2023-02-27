from django.http import JsonResponse
from django.shortcuts import render, redirect
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.urls import reverse


def healthcheck(request):
    return JsonResponse({'Status': 'API is connected!'})


def index(request):
    context = {}
    if request.user.is_authenticated:
        context = {"is_authenticated": request.user.is_authenticated, "username": request.user.username}
    return render(request, 'index.html', context)


def company(request):
    # Incomplete
    with open('data.json') as f:
        data = json.load(f)
    return render(request, 'company.html', data)


def profile(request):
    if request.user.is_authenticated:
        context = {"is_authenticated": request.user.is_authenticated, "username": request.user.username}
        return render(request, 'profile.html', context)
    else:
        return redirect('web_app:home')


@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        context = {"view": "login", "username": username, "login_error": None}
        user = authenticate(username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect('web_app:home')
        else:
            context["login_error"] = "wrong_credentials"
            return render(request, 'login.html', context)
    else:
        return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')
        context = {"view": "signup", "username": username, "first_name": first_name, "last_name": last_name,
                   "email": email, "username_error": None, "email_error": None, "password_error": None}
        # Javascript and Ajax are good for FE form validation.
        if User.objects.filter(username=username).exists():
            context["username_error"] = "already_exist"
        if User.objects.filter(email=email).exists():
            context["email_error"] = "already_exist"
        if password != confirm_password:
            context["password_error"] = "different"
        if context["username_error"] or context["email_error"] or context["password_error"]:
            return render(request, 'signup.html', context)
        else:
            user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name,
                                            last_name=last_name)
            user.save()
            auth_login(request, user)
            return redirect(reverse('web_app:home'))
    else:
        return render(request, 'signup.html')


@login_required()
def logout(request):
    auth_logout(request)
    return redirect('web_app:home')
