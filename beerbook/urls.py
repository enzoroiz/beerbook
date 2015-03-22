from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from registration.backends.simple.views import RegistrationView

from beerbookapp.models import UserProfile


# Create a new class that redirects the user to the index page, if successful at logging      
class MyRegistrationView(RegistrationView):
    def get_success_url(self,request, user):
        profile = UserProfile(user=user)

        if 'website' in request.POST:
            profile.website = request.POST["website"]
        if 'picture' in request.FILES:
            profile.picture = request.FILES["picture"]
        if 'first_name' in request.POST:
            user.first_name = request.POST["first_name"]
        if 'last_name' in request.POST:
            user.last_name = request.POST["last_name"]
        if 'bio' in request.POST:
            profile.bio = request.POST["bio"]
            
        user.save()
        profile.save()
        return '/beerbook/'
    
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'BeerBook.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^beerbook/', include('beerbookapp.urls')),
    url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
    (r'^accounts/', include('registration.backends.simple.urls')),
)


if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'^media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )