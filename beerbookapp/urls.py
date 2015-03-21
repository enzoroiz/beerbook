__author__ = 'khorm'

from django.conf.urls import patterns, url
from beerbookapp import views, views_beercat, views_events

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^event_catalogue/(?P<event_id>[\w\-]+)/$', views_events.event, name='event'),
                       url(r'^event_catalogue/$', views_events.event_catalogue, name='event_catalogue'),
                       url(r'^add_rating/$', views_beercat.add_rating, name='add_rating'),
                       url(r'^beer_catalogue/(?P<beer_name_slug>[\w\-]+)/$', views_beercat.beer, name='beer'),
                       url(r'^beer_catalogue/$', views_beercat.beer_catalogue, name='beer_catalogue'),
                       url(r'^profile/(?P<username>[\w\-]+)/$', views.profile, name='profile'),
                       url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
                       url(r'^change_password/$', views.change_password, name='change_password'),

                       )

# url(r'^$', views. , name=''),
            
