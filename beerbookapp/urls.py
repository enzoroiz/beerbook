__author__ = 'khorm'

from django.conf.urls import patterns, url
from beerbookapp import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^event_catalogue/$', views.event_catalogue, name='event_catalogue'),
                       url(r'^beer_catalogue/$', views.beer_catalogue, name='beer_catalogue'),
                       url(r'^user_profile/$', views.user_profile, name='user_profile'),

                       )

# url(r'^$', views. , name=''),