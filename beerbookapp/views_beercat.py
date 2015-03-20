__author__ = 'khorm'

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from beerbookapp.models import BeerType, Beer, Rating
from django.contrib.auth.models import User
from django.db.models import Avg
from django.db import connection
import json
# from beerbookapp.forms import BeerCatSearch


# view for adding rating to beer
def add_rating(request):

    ajax_response = "Failure"

    if request.method == 'GET':

        # print request.GET
        beer_name_slug = request.GET['beer_slug_val']
        username = request.user.username
        rating = request.GET['rating_val']
        review = request.GET['review_val']

        this_user = User.objects.get(username=username)
        this_beer = Beer.objects.get(slug=beer_name_slug)

        if not Rating.objects.filter(owner=this_user, rated_beer=this_beer).exists():
            this_rating = Rating.objects.create(owner=this_user, rated_beer=this_beer)
            this_rating.rating = rating
            this_rating.review = review
            this_rating.save()
            ajax_response = "Success"  # TODO

    response = HttpResponse(ajax_response)
    return response


# view for individual beers
def beer(request, beer_name_slug):
    context_dict = {}
    rated = False

    try:
        this_beer = Beer.objects.get(slug=beer_name_slug)

        query_string = """select P.name, L.latitude, L.longitude
                        from beerbookapp_Pub P
                        join beerbookapp_PubStockItem S
                        on S.stocked_at_id=P.id
                        join beerbookapp_Location L
                        on P.location_id=L.id
                        join beerbookapp_Beer B
                        on S.stocked_item_id=B.id
                        where B.name='""" + this_beer.name + "'"

        cursor = connection.cursor()

        try:
            cursor.execute(query_string)
            locations = cursor.fetchall()
        finally:
            cursor.close()


        rating_list = Rating.objects.filter(rated_beer=this_beer).order_by('-date')

        context_dict['beer'] = this_beer
        context_dict['rating'] = rate_beers(rating_list)
        context_dict['rating_list'] = rating_list
        context_dict['locations'] = locations

        for r in rating_list:
            if r.owner == request.user:
                rated = True
                break
    except:
        pass

    context_dict['rated'] = rated

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

        # print request.POST

        cursor = connection.cursor()
        query_string = search_query_builder(search_beer_name, search_beer_type,
                                            search_beer_rating_min, search_beer_rating_max)

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

    else:
        beer_types = BeerType.objects.all()

        query_string = ("""
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

        cursor = connection.cursor()

        try:
            cursor.execute(query_string)
            query_result = cursor.fetchall()
        finally:
            cursor.close()

        context_dict['beer_list'] = query_result
        context_dict['beer_types'] = beer_types

    response = render(request, 'beerbookapp/beer_catalogue.html', context_dict)
    return response


# helper methods ************************************************************************************


# returns beer avg rating
def rate_beers(rating_list):
    if rating_list:
        beer_ratings_number = 0
        rating_total = 0
        for rating in rating_list:
            beer_ratings_number += 1
            rating_total += rating.rating
        return rating_total / beer_ratings_number

    return None


def search_query_builder(beer_name, type_name, rating_min, rating_max):

    # convert ' in strings to SQL escape ones
    beer_name = beer_name.replace("'", "''")

    query_string = """
                        select B.slug, B.name, T.name, ROUND(AVG(R.rating), 0)
                        from beerbookapp_Beer B
                        left outer join
                        beerbookapp_Rating R
                        on B.id = R.rated_beer_id
                        left outer join
                        beerbookapp_BeerType T
                        on B.type_id = T.id """

    # check for where clause

    if beer_name:
        if type_name == 'none':
            query_string += "where LOWER(B.name) LIKE '%" + str(beer_name).lower() + "%' "
        else:
            query_string += "where "
            query_string += "LOWER(B.name) LIKE '%" + str(beer_name).lower() + "%' "
            query_string += " AND T.name == '" + str(type_name) + "' "
    elif type_name != 'none':
        query_string += "where T.name == '" + str(type_name) + "' "

    query_string += "group by B.id "

    # check for having clause
    if int(rating_min) == 0 and int(rating_max) == 0:
        pass
    elif int(rating_min) != 0 and int(rating_max) != 0:
        query_string += " having "
        query_string += " ROUND(AVG(R.rating), 0) >= "
        query_string += str(rating_min)
        query_string += " AND ROUND(AVG(R.rating), 0) <= "
        query_string += str(rating_max)
    else:
        if int(rating_min) == 0:
            query_string += " having "
            query_string += " ROUND(AVG(R.rating), 0) <= "
            query_string += str(rating_max)
            query_string += " OR ROUND(AVG(R.rating), 0) IS NULL"
        elif int(rating_max) == 0:
            query_string += " having "
            query_string += " ROUND(AVG(R.rating), 0) >= "
            query_string += str(rating_min)

    return query_string


    # used to check how the heck django names columns
    # for field in <MODELNAME>._meta.fields:
    #     print field.get_attname_column()