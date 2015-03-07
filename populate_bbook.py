#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beerbook.settings')

import datetime

import django
django.setup()

from beerbookapp.models import Beer, BeerType, BeerProducer, Event, Rating
from beerbookapp.models import Location, City, Pub, PubStockItem, FriendListItem
from django_countries import countries
from django.contrib.auth.models import User
from django.utils import timezone


def populate():

    #  beers types ******************************************************************************************
    add_beer_type("Dry Stout")
    add_beer_type("Pilsner")
    add_beer_type("Porter")
    add_beer_type("Stout")
    add_beer_type("Pale lager")
    add_beer_type("Red Ale")
    add_beer_type("American lager")

    # producers
    add_beer_producer("Anheuser Busch InBev")
    add_beer_producer("Diageo")
    add_beer_producer("Heineken International")

    # cities ***************************************************************************************
    add_city("Glasgow")
    add_city("London")
    add_city("Edinburgh")

    # locations ************************************************************************************

    city = add_city("Glasgow")
    # city, name, latitude, longitude, country
    add_location(city, "The Ben Navis", 55.864, -4.284, "GB")
    add_location(city, "George's Party Mansion", 78.864, -9.284, "GB")

    # pubs ********************************************************************************************

    location = add_location(city, "The Ben Navis", 55.864, -4.284, "GB")
    pub_desc = "Huge whisky choices and craft beers, plus live Scottish folk music in intimate pub with feature bar"
    # name, location, city, description, established
    add_pub("The Ben Navis", location, "Glasgow", pub_desc, date_me("1998"))

    # beers and pub stock ****************************************************************************************

    beer_type = add_beer_type("Dry Stout")
    producer = add_beer_producer("Diageo")
    desc = "This beer is from Dublin, Ireland. It has long been a drink of the stereotypical Irish person"
    # name, beer_type, producer, description, introduced, country
    beer = add_beer("Guiness", beer_type, producer, desc, date_me("1759"), 'IE')
    # stocked at:
    pub = add_pub("The Ben Navis", location, "Glasgow", pub_desc, date_me("1998"))
    # price, stocked_item, stocked_at
    add_pub_stock_item(5.99, beer, pub)

    beer_type = add_beer_type("American lager")
    producer = add_beer_producer("Anheuser_busch InBev")
    desc = """Known as "The King of Beers," Budweiser was first introduced by Adolphus Busch in 1876 and it's still brewed with the same high standards today.
     Budweiser is a medium-bodied, flavorful, crisp American-style lager.
     Brewed with the best barley malt and a blend of premium hop varieties, it is an icon of core American values like optimism and celebration."""
    # name, beer_type, producer, description, introduced, country
    beer = add_beer("Budweiser", beer_type, producer, desc, date_me("1876"), 'US')
    # stocked at:
    pub = add_pub("The Ben Navis", location, "Glasgow", pub_desc, date_me("1998"))
    # price, stocked_item, stocked_at
    add_pub_stock_item(2.99, beer, pub)

    beer_type = add_beer_type("Pilsner")
    producer = add_beer_producer("Anheuser_busch InBev")

    desc = """At Stella Artois, we are extremely proud of our Belgian roots.
            Our story can be seen on every bottle of Stella Artois. If you look closely, hints of our origins are
            proudly displayed.
            By 1366 roots of our brewing tradition had been established in the city of Leuven, Belgium– which is also
            where the original Den Hoorn brewery was founded. Den Hoorn laid the foundation for the quality taste and
            standard Stella Artois is known for. The symbol of the Den Hoorn Brewery is proudly displayed in Stella
            Artois' cartouche to this day.
            Sebastian Artois was admitted to the Leuven Brewer’s Guild as a Brew Master in 1708, and only nine years
            later purchased the Den Hoorn brewery. In memoriam, you can find his last name on the brewery and every
            bottle of Stella Artois around the world.
            The Artois Brewery was so beloved internationally and locally, a special batch was created as a Christmas
            gift to the people of Leuven. That special batch was the first to officially include "Stella" in its name.
            "Stella", meaning star in Latin, pays homage to this original occasion, accompanied by a star on every
            bottle.
            So next time you see a bottle of Stella Artois, take note of the rich history paired with the rich flavor
            on and in every bottle. """
    # name, beer_type, producer, description, introduced, country
    add_beer("Stella Artois", beer_type, producer, desc, date_me("1926"), 'BE')
    # stocked at:
    # price, stocked_item, stocked_at

    # users *******************************************************************************************
    # username, first_name, last_name, password
    add_user("bob", "Bob", "Bobton", "bob")
    add_user("simon", "Simon", "Beerlover", "simon")
    add_user("george", "George", "Partyanimal", "george")

    # events ******************************************************************************************
    owner = add_user("george", "George", "Partyanimal", "george")

    desc = "Everybody's invited!\n Come and join us at The Ben Navis Bar on next Friday."
    location = add_location(city, "The Ben Navis", 55.864, -4.284, "GB")
    # title, event_datetime, description, owner, location
    add_event("Friday Drinking!", datetime_me("11/11/2015 12:12"), desc, owner, location)

    desc = "All invited to my place for yet another great party!!!"
    location = add_location(city, "George's Party Mansion", 78.864, -9.284, "GB")
    # title, event_datetime, description, owner, location
    add_event("Party at Geprge's", datetime_me("12/11/2015 18:12"), desc, owner, location)

    # ratings *****************************************************************************************
    beer = get_beer("Guiness")

    owner = add_user("george", "George", "Partyanimal", "george")
    review = "This beer tasted really great! Especially for the price."
    # rating, review, owner, rated_beer
    add_rating(5, review, owner, beer)

    owner = add_user("simon", "Simon", "Beerlover", "simon")
    review = "I hated this beer, it was really disgusting. I couldn't even finish it."
    # rating, review, owner, rated_beer
    add_rating(1, review, owner, beer)

    owner = add_user("bob", "Bob", "Bobton", "bob")
    review = "This beer was average, but I guess it's good for the price."
    # rating, review, owner, rated_beer
    add_rating(3, review, owner, beer)


    # friendships

    user1 = get_user("simon")
    user2 = get_user("george")
    add_friends(user1, user2)



# ******************************
# helper methods *******************************************************************************************


def date_me(date):
    c = datetime.datetime.strptime(date, '%Y')
    return c


def datetime_me(date_time):
    c = datetime.datetime.strptime(date_time, '%d/%m/%Y %H:%M')
    c = timezone.make_aware(c, timezone.get_current_timezone())
    return c


# entity creation methods


def add_city(name):
    c = City.objects.get_or_create(name=name)[0]
    return c


def add_beer_producer(name):
    c = BeerProducer.objects.get_or_create(name=name)[0]
    return c


def add_beer_type(name):
    c = BeerType.objects.get_or_create(name=name)[0]
    return c


def add_beer(name, beer_type, producer, description, introduced, country):
    c = Beer.objects.get_or_create(name=name,
                                   type=beer_type,
                                   producer=producer,
                                   description=description,
                                   introduced=introduced,
                                   country=country)[0]
    return c


def get_beer(name):
    c = Beer.objects.get_or_create(name=name)[0]
    return c


def add_location(city, name, latitude, longitude, country):
    c = Location.objects.get_or_create(city=city,
                                       name=name,
                                       latitude=latitude,
                                       longitude=longitude,
                                       country=country)[0]
    return c


def add_pub(name, location, city, description, established):
    c = Pub.objects.get_or_create(name=name,
                                  location=location,
                                  city=city,
                                  description=description,
                                  established=established)[0]
    return c


def add_event(title, event_datetime, description, owner, location):
    c = Event.objects.get_or_create(title=title,
                                    datetime=event_datetime,
                                    description=description,
                                    owner=owner,
                                    location=location)[0]
    return c


def add_user(username, first_name, last_name, password):
    c = User.objects.get_or_create(username=username,
                                   first_name=first_name,
                                   last_name=last_name,
                                   password=password)[0]
    return c


def get_user(username):
    c = User.objects.get_or_create(username=username)[0]
    return c


def add_pub_stock_item(price, stocked_item, stocked_at):
    c = PubStockItem.objects.get_or_create(price=price,
                                           stocked_item=stocked_item,
                                           stocked_at=stocked_at)[0]
    return c


def add_rating(rating, review, owner, rated_beer):
    c = Rating.objects.get_or_create(rating=rating,
                                     review=review,
                                     owner=owner,
                                     rated_beer=rated_beer)[0]
    return c


def add_friends(user_one, user_two):
    c = FriendListItem.objects.get_or_create(user_one=user_one,
                                             user_two=user_two)[0]
    return c

# initializer ********************************************************************************

if __name__ == '__main__':
    print "\n**************************************" \
          "\nStarting BeerBook Population Script." \
          "\nHold on to your Beers!!"

    populate()
    print "\nScript End" \
          "\n**************************************\n"