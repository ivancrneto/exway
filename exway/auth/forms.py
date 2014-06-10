""" Module for forms related to authentication """

import re

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class SignUpForm(forms.Form):
    """ Form that handles user sign up """

    username = forms.CharField(max_length=30)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(), min_length=6,
                               max_length=32)

    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)

    def clean_username(self):
        """ Method for validating and cleaning username field """
        username = self.cleaned_data['username']
        if not re.match(r'^[A-Za-z0-9]+(?:[ _-][A-Za-z0-9]+)*$', username):
            raise ValidationError('Username must contain only letters, ' +
                                  'numbers, _ and -')
        user = User.objects.filter(username=username)
        if user:
            raise ValidationError('There is already an user with this ' +
                                  'username.')
        return username

    def clean_email(self):
        """ Method for validating and cleaning the email field """
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email)
        if user:
            raise ValidationError('There is already an user with this email.')

        return email

    def clean_first_name(self):
        """ Method for validating and cleaning the first_name field """
        first_name = self.cleaned_data['first_name']
        if not re.match(r'^[\w]+$', first_name):
            raise ValidationError('First Name must contain only letters.')

        return first_name

    def clean_last_name(self):
        """ Method for validating and cleaning the last_name field """
        last_name = self.cleaned_data['last_name']
        if not re.match(r'^[\w]+$', last_name):
            raise ValidationError('Last Name must contain only letters.')

        return last_name
