__author__ = 'khorm'
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from beerbookapp.models import Event, Location

@login_required
def add_event(request):

    success = False
    context_dict ={}

    if request.method == 'POST':
        this_user = request.username
        
        pass
    else:


        try:
            # send form with locations
            this_location = Location.objects.all()
            context_dict['locations'] = this_location
        except:
            pass

    print context_dict


    response = render(request, 'beerbookapp/add_event.html', context_dict)
    return response



def event(request, event_id):
    context_dict = {}

    # print event_id

    try:
        this_event = Event.objects.get(id=event_id)
        # print this_event
        context_dict['event'] = this_event
    except:
        pass

    response = render(request, 'beerbookapp/event.html', context_dict)
    return response


def event_catalogue(request):

    context_dict = {}

    sql_query = "select E.title, E.datetime, U.username, E.id " \
                "from beerbookapp_Event E " \
                "join auth_user U " \
                "on E.owner_id = U.id " \
                "order by E.datetime"

    cursor = connection.cursor()

    try:
        cursor.execute(sql_query)
        context_dict['events_list'] = cursor.fetchall()
        # print context_dict
    finally:
        cursor.close()



    response = render(request, 'beerbookapp/event_catalogue.html', context_dict)
    return response

