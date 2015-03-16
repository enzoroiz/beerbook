__author__ = 'khorm'

from django.conf.urls import patterns, url
from beerbookapp import views, views_beercat

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^event_catalogue/$', views.event_catalogue, name='event_catalogue'),

                       url(r'^beer_catalogue/(?P<beer_name_slug>[\w\-]+)/$', views_beercat.beer, name='beer'),
                       url(r'^beer_catalogue/$', views_beercat.beer_catalogue, name='beer_catalogue'),
                       url(r'^user_profile/$', views.user_profile, name='user_profile'),


                       )

# url(r'^$', views. , name=''),

