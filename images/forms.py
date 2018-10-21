"""
This file powers creation of all forms. You will need to modify
the SignUpForm in order to start collecting the distinct_id.
"""

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
