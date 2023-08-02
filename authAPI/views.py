# myapp/views.py

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.decorators import api_view

from rest_framework.response import Response
import re

@api_view(['POST'])
def register_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    username = request.data.get('username')
    
    if not email or not password:
        return JsonResponse({'error': 'Email and password are required.'}, status=400)

    # Check email format
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return JsonResponse({'error': 'Invalid email format.'}, status=400)

    # Check if the email is already registered
    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Username is already taken.'}, status=400)
    if User.objects.filter(email=email).exists():
        return JsonResponse({'error': 'Email is already registered.'}, status=400)

    # Create a new user
    user = User.objects.create_user(username=username, email=email, password=password)
    return JsonResponse({'message': 'Registration successful.'}, status=201)

@api_view(['POST'])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    if not email or not password:
        return JsonResponse({'error': 'Email and password are required.'}, status=400)

    user = authenticate(username=email, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({'message': 'Login successful.'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid email or password.'}, status=401)
