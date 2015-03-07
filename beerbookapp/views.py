from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.


def index(request):
    response = render(request, 'beerbookapp/index.html')
    return response


def beer_catalogue(request):
    response = render(request, 'beerbookapp/beer_catalogue.html')
    return response


def user_profile(request):
    response = render(request, 'beerbookapp/user_profile.html')
    return response


def event_catalogue(request):
    response = render(request, 'beerbookapp/event_catalogue.html')
    return response
