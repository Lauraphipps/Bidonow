import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User


@csrf_exempt
def signup(request):
    data = json.loads(request.body)
    email = data['email']
    password = data['password']
    username = email
    user = User.objects.create_user(username, email, password)
    user.save()
    return JsonResponse({'success': True})
