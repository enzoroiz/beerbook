__author__ = 'khorm'

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from beerbookapp.models import BeerType, Beer
#from beerbookapp.forms import BeerCatSearch


def beer(request, beer_name_slug):

    context_dict = {}

    try:
        this_beer = Beer.objects.get(slug=beer_name_slug)
        context_dict['beer'] = this_beer

    except:
        pass

    response = render(request, 'beerbookapp/beer.html', context_dict)
    return response


def beer_catalogue(request):

    context_dict = {}

    if request.method == 'POST':
        # print request
        if 'beername' in request.POST:

            beer_name = request.POST['beername']


            try:
                beer = Beer.objects.get(name=beer_name)
                context_dict['search_beer'] = beer
            except:
                pass

    else:
        beer_types = BeerType.objects.all()
        beer_list = Beer.objects.all()
        context_dict['beer_types'] = beer_types
        context_dict['beer_list'] = beer_list

    response = render(request, 'beerbookapp/beer_catalogue.html', context_dict)
    return response