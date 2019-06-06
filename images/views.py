from django.contrib.auth import authenticate
from django.contrib.auth import login as log_in
from django.contrib.auth import logout as log_out
from django.http import HttpResponseRedirect
from django.shortcuts import render

from images.forms import SignUpForm
from images.forms import LoginForm

from mixpanel import Mixpanel
import datetime
mp = Mixpanel("84849055535b43f7d7b2022b6ca224c9")


def index(request):
    """Return the logged in page, or the logged out page
    """
    print('Index view!')
    """mp_distinct_id = get_distinct_id(request)"""

    if request.user.is_authenticated():
        return render(request, 'images/index-logged-in.html', {
            'user': request.user,
            'email': request.user.email,
            'username': request.user.username
        })
    else:
        return render(request, 'images/index-logged-out.html')


def signup(request):
    """Render the Signup form or a process a signup
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        username = request.POST['username']
        now = datetime.datetime.utcnow()

        if form.is_valid():
            mp_did = request.POST['mp_distinct_id']
            mp.track(mp_did,"Sign up", {
                "Username": username,
                "Signup Date" : now.strftime("%Y-%m-%dT%H:%M:%S")

            })

            now = datetime.datetime.utcnow()
            email = form.cleaned_data.get('email')
            name = form.cleaned_data.get('first_name')
            username = form.cleaned_data.get('username')

            mp.alias(email, mp_did)

            mp.people_set(mp_did, {
                '$first_name' : name,
                'Signup Date' : now.strftime("%Y-%m-%dT%H:%M:%S"),
                '$email' : email,
                '$username' : username,
                'Number of Logins' : 0,
                'Number of Corgis' : 0,
            })

            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            log_in(request, user)
            return HttpResponseRedirect('/')

    else:
        form = SignUpForm()

    return render(request, 'images/signup.html', {'form': form})

    # Tracks signup event
    #mp.track('123', 'signup')


def login(request):
    """Render the login form or log in the user
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            now = datetime.datetime.utcnow()

            log_in(request, user)

            mp.track(request.user.email, "Login", {
                "Username": username
            })

            mp.people_increment(request.user.email, {
                'Number of Logins': 1
                })
            mp.people_set(request.user.email, {
                'Corgis' : 'yes please',
                'Last Login' : now.strftime("%Y-%m-%dT%H:%M:%S")
                })
            
            return HttpResponseRedirect('/')
        else:
            return render(request, 'images/login.html', {
                'form': LoginForm,
                'error': 'Please try again'
            })
    else:
        return render(request, 'images/login.html', {'form': LoginForm})



def logout(request):
    """Logout the user
    """
    log_out(request)
    return HttpResponseRedirect('/')
