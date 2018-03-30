import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout



@csrf_exempt
def signup(request):
    data = json.loads(request.body)
    email = data['email']
    password = data['password']
    username = email
    user = User.objects.create_user(username, email, password)
    user.save()
    return JsonResponse({'success': True})


@csrf_exempt
def login_view(request):
    data = json.loads(request.body)
    email = data['email']
    password = data['password']
    username = email
    result = False
    user = authenticate(request, username=username, password=password)
    if user is not None:
        result = True
        login(request, user)
    return JsonResponse({'success': result})


@csrf_exempt
def logout_view(request):
    logout(request)
    return JsonResponse({})


def secure_page(request):
    return HttpResponse('This is secure page requied 2FA')
