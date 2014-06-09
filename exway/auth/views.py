from django.contrib.auth.models import User
from django.contrib.auth import login as _login, logout as _logout
from django.core.urlresolvers import reverse as r
from django.shortcuts import render, redirect
from django.db.models import Q
from exway.auth.forms import SignUpForm


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {})

    signup_form = SignUpForm(request.POST)
    if signup_form.is_valid():
        data = signup_form.cleaned_data
        user = User(first_name=data['first_name'], last_name=data['last_name'],
                    email=data['email'], username=data['username'],
                    is_active=True)
        user.set_password(data['password'])
        user.save()
        request.session['signup_username'] = user.username
        return redirect(r('auth:login'))
    else:
        return render(request, 'signup.html', {'form': signup_form})


def login(request):
    if request.user.is_authenticated():
        return redirect(r('core:home'))

    if request.method == 'GET':
        context = {}
        if 'signup_username' in request.session:
            context['signup_username'] = request.session.pop('signup_username')
        return render(request, 'login.html', context)

    try:
        user = User.objects.get(Q(username=request.POST['username']) |
                                Q(email=request.POST['username']))
    except User.DoesNotExist:
        return render(request, 'login.html', {})

    if user.check_password(request.POST['password']):
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        _login(request, user)
        request.session.set_expiry(60 * 60 * 10000000)
        return redirect(request.GET.get('next', r('core:home')))
    else:
        return render(request, 'login.html', {})


def logout(request):
    _logout(request)
    return redirect(r('core:home'))
