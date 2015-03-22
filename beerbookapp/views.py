from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from beerbookapp.models import Pub, Beer, PubStockItem, UserProfile


# Create your views here.
def index(request):

    context_dict = {}

    sql_query = "select B.slug, B.name , B.image, substr(B.description, 1, 217), ROUND(AVG(R.rating), 0) " \
                "from beerbookapp_Beer B " \
                " left outer join beerbookapp_Rating R on B.id = R.rated_beer_id" \
                " group by B.id" \
                " order by ROUND(AVG(R.rating), 0) desc " \
                "LIMIT 5"

    sql_query1 = "select E.title, E.datetime, U.username " \
                "from beerbookapp_Event E " \
                "join auth_user U " \
                "on E.owner_id = U.id " \
                "order by E.datetime " \
                "LIMIT 3"

    cursor = connection.cursor()

    try:
        cursor.execute(sql_query)
        context_dict['top_beers'] = cursor.fetchall()
        cursor.execute(sql_query1)
        context_dict['recent_events'] = cursor.fetchall()
        # print context_dict
    finally:
        cursor.close()

    response = render(request, 'beerbookapp/index.html', context_dict)
    return response


def user_profile(request):
    response = render(request, 'beerbookapp/user_profile.html')
    return response


@login_required
def profile(request, username):
    act_user = User.objects.get(username=username)
    userprofile, created = UserProfile.objects.get_or_create(user=act_user)
    
    if request.method == 'POST':
        if 'is_password' in request.POST:
            # print "IS_PASSWORD"
            data = {}
            if 'old_password' in request.POST:
                data['old_password'] = request.POST['old_password']
            if 'new_password1' in request.POST:
                data['new_password1'] = request.POST['new_password1']
            if 'new_password2' in request.POST:
                data['new_password2'] = request.POST['new_password2']
            form = PasswordChangeForm(act_user, data)
            if form.is_valid():
                form.save(commit=True)
                act_user.save()
                user = authenticate(username=username, password=data['new_password1'])
                login(request, user)
                messages.success(request, 'Password changed.')
                # print messages
                return render(request, 'beerbookapp/profile.html', {'userprofile': userprofile, 'act_user': act_user, 'user':user })
            else:
                if form.errors:
                    print form.errors
                return render(request, 'beerbookapp/profile.html', {'userprofile': userprofile, 'act_user': act_user, 'user':act_user, 'form':form})
        else:
            if 'email' in request.POST:
                act_user.email = request.POST['email']
            if 'website' in request.POST:
                userprofile.website = request.POST["website"]
            if 'picture' in request.FILES:
                userprofile.picture = request.FILES["picture"]
            
            userprofile.save()
            act_user.save()
            messages.success(request, 'Profile details updated.')   
    
    return render(request, 'beerbookapp/profile.html', {'userprofile': userprofile, 'act_user': act_user })

@login_required
def edit_profile(request):
    user = request.user
    userprofile = UserProfile.objects.get(user=user)
    return render(request, 'beerbookapp/edit_profile.html', {'user':user, 'userprofile':userprofile})

@login_required
def change_password(request):
    user = request.user
    userprofile = UserProfile.objects.get(user=user)
    return render(request, 'beerbookapp/change_password.html', {'user':user, 'userprofile':userprofile})

@login_required
def users_profiles(request):
    user_list = User.objects.all().order_by('id')
    userprofile_list = UserProfile.objects.all().order_by('user')
    print user_list
    print userprofile_list
    user_data = zip(user_list, userprofile_list)
    return render(request, 'beerbookapp/users_profiles.html', {'user_list' : user_list, 'user_data' : user_data})