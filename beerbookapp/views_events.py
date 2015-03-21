__author__ = 'khorm'
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render


def event_catalogue(request):

    context_dict = {}

    sql_query = "select E.title, E.datetime, U.username " \
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

