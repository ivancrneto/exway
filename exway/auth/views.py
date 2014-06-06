from django.contrib.auth.models import User
from django.shortcuts import render

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html', {})
