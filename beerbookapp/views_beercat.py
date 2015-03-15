__author__ = 'khorm'

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from beerbookapp.models import BeerType, Beer, Rating
#from beerbookapp.forms import BeerCatSearch


def beer(request, beer_name_slug):

    context_dict = {}

    try:
        this_beer = Beer.objects.get(slug=beer_name_slug)
        context_dict['beer'] = this_beer

        rating_list = Rating.objects.filter(rated_beer=this_beer)
        context_dict['rating'] = rate_beers(rating_list)

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
                beer_dict = Beer.objects.get(name=beer_name)
                context_dict['search_beer'] = beer_dict
            except:
                pass

    else:
        beer_types = BeerType.objects.all()
        beer_list = Beer.objects.all()

        for this_beer in beer_list:
            rating_list = Rating.objects.filter(rated_beer=this_beer)
            this_beer.avgrating = (rate_beers(rating_list))



        print beer_list
        # context_dict['beer_ratings'] = rating_dict
        # context_dict['beer_list'] = beer_list

        context_dict['beer_list'] = beer_list
        context_dict['beer_types'] = beer_types
        print context_dict

    response = render(request, 'beerbookapp/beer_catalogue.html', context_dict)
    return response


# helper methods ************************************************************************************


def rate_beers(rating_list):
    if rating_list:
            beer_ratings_number = 0
            rating_total = 0
            for rating in rating_list:
                beer_ratings_number += 1
                rating_total += rating.rating
            return rating_total / beer_ratings_number

    return None