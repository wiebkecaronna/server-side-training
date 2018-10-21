from django.contrib.auth import authenticate
from django.contrib.auth import login as log_in
from django.contrib.auth import logout as log_out
from django.http import HttpResponseRedirect
from django.shortcuts import render

from images.forms import SignUpForm


def index(request):
    """Return the logged in page, or the logged out page
    """
    if request.user.is_authenticated():
        return render(request, 'images/index-logged-in.html', {
            'user': request.user
        })
    else:
        return render(request, 'images/index-logged-out.html')


def signup(request):
    """Sign up the user
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            log_in(request, user)
            return HttpResponseRedirect('/')

    else:
        form = SignUpForm()

    return render(request, 'images/signup.html', {'form': form})


def login(request):
    """Login the user
    """
    log_in(request)
    return HttpResponseRedirect('/')


def logout(request):
    """Logout the user
    """
    log_out(request)
    return HttpResponseRedirect('/')
