from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from beerbookapp.models import Pub, Beer, PubStockItem

# Create your views here.


def index(request):
    response = render(request, 'beerbookapp/index.html')
    return response


def user_profile(request):
    response = render(request, 'beerbookapp/user_profile.html')
    return response


def event_catalogue(request):

    # cursor = connection.cursor()
    # beer_name = "Guiness"
    # cursor.execute(""" select P.name
    #                 from beerbookapp_Pub P
    #                 join
    #                 beerbookapp_PubStockItem S
    #                 on S.stocked_at_id=P.id
    #                 join
    #                 beerbookapp_Beer B
    #                 on S.stocked_item_id=B.id
    #                 where B.name='""" + beer_name + "'")
    # query_result = cursor.fetchall()
    # print query_result


    response = render(request, 'beerbookapp/event_catalogue.html')
    return response
