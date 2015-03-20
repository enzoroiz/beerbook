__author__ = 'khorm'

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from beerbookapp.models import BeerType, Beer, Rating
from django.contrib.auth.models import User
from django.db.models import Avg
from django.db import connection
import json
#from beerbookapp.forms import BeerCatSearch


# view for adding rating to beer
def add_rating(request):

    # beer_name_slug = None
    # username = None
    # rating = None
    # review = None
    ajax_response = "Failure"

    if request.method == 'GET':

        # print request.GET
        beer_name_slug = request.GET['beer_slug_val']
        username = request.user.username
        rating = request.GET['rating_val']
        review = request.GET['review_val']

        # print beer_name_slug
        # print username
        # print review
        # print rating
        this_user = User.objects.get(username=username)
        this_beer = Beer.objects.get(slug=beer_name_slug)

        if not Rating.objects.filter(owner=this_user, rated_beer=this_beer).exists():
            this_rating = Rating.objects.create(owner=this_user, rated_beer=this_beer)
            this_rating.rating = rating
            this_rating.review = review
            this_rating.save()
            ajax_response = "Success"

        # username = request.user.username

    response = HttpResponse(ajax_response)
    return response


# view for individual beers
def beer(request, beer_name_slug):

    context_dict = {}

    try:
        this_beer = Beer.objects.get(slug=beer_name_slug)
        context_dict['beer'] = this_beer

        rating_list = Rating.objects.filter(rated_beer=this_beer).order_by('-date')[:4]
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

        search_beer_type = request.POST['beertype']
        search_beer_name = request.POST['beername']
        search_beer_rating_max = request.POST['ratingmax']
        search_beer_rating_min = request.POST['ratingmin']

        # convert ' in strings to SQL escape ones
        search_beer_name = search_beer_name.replace("'", "''")


        # print "IN POST"
        # print request.POST
        # print ""

        cursor = connection.cursor()
        query_string = """
                        select B.slug, B.name, T.name, ROUND(AVG(R.rating), 0)
                        from beerbookapp_Beer B
                        left outer join
                        beerbookapp_Rating R
                        on B.id = R.rated_beer_id
                        left outer join
                        beerbookapp_BeerType T
                        on B.type_id = T.id """

        if search_beer_name:
            query_string += """where LOWER(B.name) LIKE '%""" + str(search_beer_name).lower() + "%' "

        query_string += "group by B.id "

        if int(search_beer_rating_min) == 0 and int(search_beer_rating_max) == 0:
            pass
        elif int(search_beer_rating_min) != 0 and int(search_beer_rating_max) != 0:
            query_string += " having "
            query_string += " ROUND(AVG(R.rating), 0) >= "
            query_string += str(search_beer_rating_min)
            query_string += " AND ROUND(AVG(R.rating), 0) <= "
            query_string += str(search_beer_rating_max)
        else:
            if int(search_beer_rating_min) == 0:
                query_string += " having "
                query_string += " ROUND(AVG(R.rating), 0) <= "
                query_string += str(search_beer_rating_max)
                query_string += " OR ROUND(AVG(R.rating), 0) IS NULL"
            elif int(search_beer_rating_max) == 0:
                query_string += " having "
                query_string += " ROUND(AVG(R.rating), 0) >= "
                query_string += str(search_beer_rating_min)



        # print "\n"
        # print query_string

        try:
            cursor.execute(query_string)
            query_result = cursor.fetchall()
        finally:
            cursor.close()

        # print "\n"
        # print query_result


        beer_types = BeerType.objects.all()
        context_dict['beer_types'] = beer_types
        context_dict['beer_list'] = query_result

        # # print request
        # if 'beername' in request.POST:
        #
        #     beer_name = request.POST['beername']
        #
        #     try:
        #         beer_dict = Beer.objects.get(name=beer_name)
        #         context_dict['search_beer'] = beer_dict
        #     except:
        #         pass
    else:
        beer_types = BeerType.objects.all()

        print "IN ELSE"
        cursor = connection.cursor()
        cursor.execute("""
                        select B.slug, B.name, T.name, ROUND(AVG(R.rating), 0)
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