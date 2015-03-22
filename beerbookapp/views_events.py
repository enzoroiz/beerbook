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
import datetime
from django.utils import timezone


@login_required
def add_event(request):

    success = False
    context_dict ={}

    if request.method == 'POST':

        print request.POST

        time_h = int(request.POST.get('ev_time-h', None))
        time_m = int(request.POST.get('ev_time-m', None))
        date = request.POST.get('ev_date', None)
        loc = request.POST.get('ev_location', None)
        desc = request.POST.get('ev_desc', None)
        title = request.POST.get('ev_title', None)
        p_date = None
        username = request.user.username

        if time_h and time_m and date:
            p_date = datetime_me(date, time_h, time_m)

        try:
            print "TRY"
            if not Event.objects.filter(title=title, datetime=p_date).exists():

                print "IF NOT"
                print p_date
                print desc
                print title


                this_user = User.objects.get(username=username)
                print this_user
                this_location = Location.objects.get(id=loc)
                print this_location
                this_event = Event.objects.create(owner=this_user, location=this_location, datetime=p_date)
                print this_event
                this_event.title = title
                this_event.description = desc
                this_event.save()
                return HttpResponseRedirect('/beerbook/event_catalogue/' + str(this_event.id))
            else:
                response = render(request, 'beerbookapp/add_event.html', {'ev_error': 'Event already exists'})
                return response

        except:
            pass



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


# helper methods *******************************************

def datetime_me(date, hours, minutes):
    c = datetime.datetime.strptime(date, '%d/%m/%Y')
    c = c.replace(hour=hours, minute=minutes)
    c = timezone.make_aware(c, timezone.get_current_timezone())
    return c