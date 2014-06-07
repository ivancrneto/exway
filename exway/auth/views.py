from django.contrib.auth.models import User
from django.contrib.auth import login as _login, logout as _logout
from django.shortcuts import render, redirect


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html', {})

    try:
        user = User.objects.get(username=request.POST['username'])
        if user.check_password(request.POST['password']):
            user.backend='django.contrib.auth.backends.ModelBackend'
            _login(request, user)
            request.session.set_expiry(60 * 60 * 10000000)
            return redirect(request.GET.get('next', '/'))
        else:
            return render(request, 'login.html', {})
    except User.DoesNotExist:
        return render(request, 'login.html', {})


def logout(request):
    _logout(request)
    return redirect('/')
