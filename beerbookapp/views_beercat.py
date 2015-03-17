__author__ = 'khorm'

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from beerbookapp.models import BeerType, Beer, Rating
from django.contrib.auth.models import User
from django.db.models import Avg
from django.db import connection
#from beerbookapp.forms import BeerCatSearch


# view for adding rating to beer
def add_rating(request):

    beer_name_slug = None
    username = None
    rating = None
    review = None

    if request.method == 'GET':
        beer_name_slug = request.GET['beer_slug']
        this_beer = Beer.objects.get(slug=beer_name_slug)
        username = request.GET['username']
        this_user = User.objects.get(username=username)
        if not Rating.objects.filter(owner=this_user, rated_beer=this_beer).exists():
            print "doesnt exist"  # create and save to db
        else:
            print str(Rating.objects.filter(owner=this_user, rated_beer=this_beer))

        # username = request.user.username

    response = HttpResponse()
    return response


# view for individual beers
def beer(request, beer_name_slug):

    context_dict = {}

    try:
        this_beer = Beer.objects.get(slug=beer_name_slug)
        context_dict['beer'] = this_beer

        rating_list = Rating.objects.filter(rated_beer=this_beer)
        context_dict['rating'] = rate_beers(rating_list)
        context_dict['rating_list'] = rating_list

    except:
        pass

    response = render(request, 'beerbookapp/beer.html', context_dict)
    return response


# view for beer catalogue
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

        cursor = connection.cursor()
        cursor.execute("""
                        select B.slug, B.name, T.name, AVG(R.rating)
                        from beerbookapp_Beer B
                        left outer join
                        beerbookapp_Rating R
                        on B.id = R.rated_beer_id
                        left outer join
                        beerbookapp_BeerType T
                        on B.type_id = T.id
                        group by B.id
                        """)
        query_result = cursor.fetchall()

        context_dict['beer_list'] = query_result
        context_dict['beer_types'] = beer_types

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


# used to check how the heck django names columns
        # for field in <MODELNAME>._meta.fields:
        #     print field.get_attname_column()