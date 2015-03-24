from django.test import TestCase
from beerbookapp.models import Rating, Location, City, Beer, BeerType, BeerProducer, Event
from datetime import datetime
from django_countries.fields import CountryField
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.urlresolvers import reverse


class TestEventCataloguePage(TestCase):

    def test_event_catalogue_with_no_events(self):

        response = self.client.get(reverse('event_catalogue'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No Events found")
        self.assertQuerysetEqual(response.context['events_list'], [])

    def test_event_catalogue_with_events_present(self):

        make_test_event_stub()

        response = self.client.get(reverse('event_catalogue'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Event")
        num_beers = len(response.context['events_list'])
        self.assertEquals(num_beers, 1)


class TestBeerCataloguePage(TestCase):

    def test_beer_catalogue_with_no_beers(self):

        response = self.client.get(reverse('beer_catalogue'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No beers matching the criteria found")
        self.assertQuerysetEqual(response.context['beer_list'], [])

    def test_beer_catalogue_with_beers(self):

        make_test_beer_stub()

        response = self.client.get(reverse('beer_catalogue'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Beer")
        num_beers = len(response.context['beer_list'])
        self.assertEquals(num_beers, 1)


class TestIndexPage(TestCase):

    def test_index_page_without_beers(self):

        # top_beers
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No beers found in database.")
        self.assertQuerysetEqual(response.context['top_beers'], [])

    def test_index_page_without_events(self):

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Unfortunately there are no upcoming events.")
        self.assertQuerysetEqual(response.context['recent_events'], [])


class TestStubsUser(TestCase):

    def test_user_stub(self):
        stub_user = make_test_user_stub()
        self.assertEquals((stub_user.username == "test"), True)

    def test_beer_type_stub(self):
        stub_beer_type = make_test_beer_type_stub()
        self.assertEquals((stub_beer_type.name == "Test Brew"), True)

    def test_beer_producer(self):
        stub_beer_producer = make_test_beer_producer_stub()
        self.assertEquals((stub_beer_producer.name == "Test Beer Producer"), True)

    def test_beer_stub(self):
        stub_beer = make_test_beer_stub()
        self.assertEquals((stub_beer.name == "Test Beer"), True)

    def test_rating_stub(self):
        stub_rating = make_test_rating_stub()
        self.assertEquals((stub_rating.rating == 0), True)


class UserMethodTest(TestCase):
    username = "test"
    first_name = "Tester"
    last_name = "Testington"
    password = "test"

    def test_ensure_user_is_created(self):

        this_user = make_test_user(self.username,
                                   self.first_name,
                                   self.last_name,
                                   self.password)
        this_user.save()

        self.assertEqual((this_user.username == self.username), True)
        self.assertEqual((this_user.first_name == self.first_name), True)
        self.assertEqual((this_user.last_name == self.last_name), True)
        self.assertEqual((this_user.password == self.password), True)


class BeerTypeMethodTest(TestCase):

    beer_type_name = "Test Brew"

    def test_ensure_beer_type_is_created(self):

        this_beer_type = make_test_beer_type(self.beer_type_name)
        this_beer_type.save()

        self.assertEquals((this_beer_type.name == self.beer_type_name), True)


class BeerProducerMethodTest(TestCase):

    producer_name = "Test Beer Producer"

    def test_ensure_beer_producer_is_created(self):

        this_beer_producer = make_test_beer_producer(self.producer_name)
        this_beer_producer.save()

        self.assertEquals((this_beer_producer.name == self.producer_name), True)


class BeerMethodTest(TestCase):

    beer_name = "Test Beer"
    beer_introduced = datetime.now()
    beer_desc = "test beer description"
    beer_country = 'GB'

    def test_ensure_beer_is_created(self):

        beer_type = make_test_beer_type_stub()
        beer_producer = make_test_beer_producer_stub()

        # name, b_type, producer, description, introduced, country
        this_beer = make_test_beer(self.beer_name,
                                   beer_type,
                                   beer_producer,
                                   self.beer_desc,
                                   self.beer_introduced,
                                   self.beer_country)
        this_beer.save()

        self.assertEquals((this_beer.name == self.beer_name), True)
        self.assertEquals((this_beer.type == beer_type), True)
        self.assertEquals((this_beer.producer == beer_producer), True)
        self.assertEquals((this_beer.description == self.beer_desc), True)
        self.assertEquals((this_beer.introduced == self.beer_introduced), True)
        self.assertEquals((this_beer.country == self.beer_country), True)

    def test_ensure_slug_is_created(self):

        this_beer = make_test_beer_stub()
        self.assertEquals((this_beer.slug == "test-beer"), True)


class LocationMethodTest(TestCase):

    loc_name = "Test Place"
    loc_latitude = 10.000
    loc_longitude = 10.000
    loc_country = 'GB'

    def test_ensure_location_is_created(self):

        loc_city = make_test_city_stub()

        this_location = make_test_location(loc_city,
                                           self.loc_name,
                                           self.loc_latitude,
                                           self.loc_longitude,
                                           self.loc_country)
        this_location.save()

        self.assertEquals((this_location.name == self.loc_name), True)


class RatingMethodTest(TestCase):

    r_rating = 1
    r_review = "Test beer review"
    r_date = datetime.now()

    def test_ensure_rating_is_created(self):

        r_beer = make_test_beer_stub()
        r_owner = make_test_user_stub()
        this_rating = make_test_rating(self.r_rating, self.r_review, r_owner, r_beer)
        this_rating.save()

        self.assertEquals((this_rating.rating == self.r_rating), True)

    def test_ensure_rating_not_saved_negative_values(self):

        r_beer = make_test_beer_stub()
        r_owner = make_test_user_stub()
        this_rating = make_test_rating(-1, self.r_review, r_owner, r_beer)
        this_test = this_rating.save()

        self.assertEquals((this_test is None), True)

    def test_ensure_rating_not_saved_out_of_range_values(self):

        r_beer = make_test_beer_stub()
        r_owner = make_test_user_stub()
        this_rating = make_test_rating(6, self.r_review, r_owner, r_beer)
        this_test = this_rating.save()

        self.assertEquals((this_test is None), True)

    def test_ensure_unique_together_holds(self):

        r_beer = make_test_beer_stub()
        r_owner = make_test_user_stub()

        this_rating1 = make_test_rating(self.r_rating, self.r_review, r_owner, r_beer)
        this_rating1.save()
        this_rating_bad = None

        with self.assertRaises(IntegrityError):
            this_rating2 = make_test_rating(self.r_rating, self.r_review, r_owner, r_beer)
            this_rating_bad = this_rating2.save()

        self.assertEquals((this_rating1 is None), False)
        self.assertEquals((this_rating_bad is None), True)





# helper methods**********************************************************************


def make_test_user(username, first_name, last_name, password):
    c = User(username=username,
             first_name=first_name,
             last_name=last_name,
             password=password)
    return c


def make_test_user_stub():
    username = "test"
    first_name = "Tester"
    last_name = "Testington"
    password = "test"

    c = make_test_user(username, first_name, last_name, password)
    c.save()
    return c


def make_test_city_stub():
    name = "Test City"
    c = make_test_city(name)
    c.save()
    return c


def make_test_city(name):
    c = City(name=name)
    return c


def make_test_location(city, name, latitude, longitude, country):
    c = Location(city=city,
                 name=name,
                 latitude=longitude,
                 longitude=latitude,
                 country=country)

    return c


def make_test_location_stub():
    city = make_test_city_stub()
    name = "Test Location"
    latitude = 10.00
    longitude = 10.00
    country = 'GB'
    c = make_test_location(city, name, latitude, longitude, country)
    c.save()
    return c


def make_test_beer(name, b_type, producer, description, introduced, country):
    c = Beer(name=name,
             type=b_type,
             producer=producer,
             description=description,
             introduced=introduced,
             country=country
             )
    return c


def make_test_beer_stub():
    name = "Test Beer"
    b_type = make_test_beer_type_stub()
    producer = make_test_beer_producer_stub()
    description = "This is a test beer"
    introduced = datetime.now()
    country = 'GB'

    c = make_test_beer(name, b_type, producer, description, introduced, country)
    c.save()
    return c


def make_test_beer_type_stub():
    c = make_test_beer_type("Test Brew")
    c.save()
    return c


def make_test_beer_type(name):
    c = BeerType(name=name)
    return c


def make_test_beer_producer_stub():
    name = "Test Beer Producer"
    c = make_test_beer_producer(name)
    c.save()
    return c


def make_test_beer_producer(name):
    c = BeerProducer(name=name)
    return c


def make_test_rating(rating, review, owner, rated_beer):
    c = Rating(rating=rating,
               review=review,
               owner=owner,
               rated_beer=rated_beer)
    return c


def make_test_rating_stub():
    rating = 0
    review = "Test Review!"
    owner = make_test_user_stub()
    rated_beer = make_test_beer_stub()
    c = make_test_rating(rating, review, owner, rated_beer)
    c.save()
    return c


def make_test_event(title, event_datetime, description, owner, location):
    c = Event(title=title,
              datetime=event_datetime,
              description=description,
              owner=owner,
              location=location)
    return c


def make_test_event_stub():
    title = "Test Event"
    e_datetime = datetime.now()
    description = "Description of Test Event"
    owner = make_test_user_stub()
    location = make_test_location_stub()
    c = make_test_event(title, e_datetime, description, owner, location)
    c.save()

    return c












