# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from giggle_app.forms import AuthenticateForm, UserCreateForm, RibbitForm
from giggle_app.models import Ribbit
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

def index(request, auth_form=None, user_form=None):
    # User is logged in
    if request.user.is_authenticated():
        ribbit_form = RibbitForm()
        user = request.user
        ribbits_self = Ribbit.objects.filter(user=user.id)
        ribbits_buddies = Ribbit.objects.filter(user__userprofile__in=user.profile.follows.all)
        ribbits = ribbits_self | ribbits_buddies
 
        return render(request,
                      'buddies.html',
                      {'ribbit_form': ribbit_form, 'user': user,
                       'ribbits': ribbits,
                       'next_url': '/', })
    else:
        # User is not logged in
        auth_form = auth_form or AuthenticateForm()
        user_form = user_form or UserCreateForm()
 
        return render(request,
                      'home.html',
                      {'auth_form': auth_form, 'user_form': user_form, })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticateForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            # Success
            return redirect('/')
        else:
            # Failure
            return index(request, auth_form=form)
    return redirect('/')
 
 
def logout_view(request):
    logout(request)
    return redirect('/')

def signup(request):
    user_form = UserCreateForm(data=request.POST)
    if request.method == 'POST':
        if user_form.is_valid():
            username = user_form.clean_username()
            password = user_form.clean_password2()
            user_form.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        else:
            return index(request, user_form=user_form)
    return redirect('/')
	

@login_required
def submit(request):
    if request.method == "POST":
        ribbit_form = RibbitForm(data=request.POST)
        next_url = request.POST.get("next_url", "/")
        if ribbit_form.is_valid():
            ribbit = ribbit_form.save(commit=False)
            ribbit.user = request.user
            ribbit.save()
            return redirect(next_url)
        else:
            return public(request, ribbit_form)
    return redirect('/')
	
@login_required
def public(request, ribbit_form=None):
    ribbit_form = ribbit_form or RibbitForm()
    ribbits = Ribbit.objects.reverse()[:10]
    return render(request,
                  'public.html',
                  {'ribbit_form': ribbit_form, 'next_url': '/giggles',
                   'ribbits': ribbits, 'username': request.user.username})

 
def get_latest(user):
    try:
        return user.ribbit_set.order_by('-id')[0]
    except IndexError:
        return ""
 
#if no username is given in the url, we fetch a list of all the users and use the annotate() function to add a ribbit_count attribute to all objects, which stores the number of giggles made by each user in the queryset. This allows us to use something along the lines of <user_object>.ribbit_count to fetch the giggle Count of the user.				   
 
@login_required
def users(request, username="", ribbit_form=None):
    if username:
        # Show a profile
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404
        ribbits = Ribbit.objects.filter(user=user.id)
        if username == request.user.username or request.user.profile.follows.filter(user__username=username):
            # Self Profile or buddies' profile
            return render(request, 'user.html', {'user': user, 'ribbits': ribbits, })
        return render(request, 'user.html', {'user': user, 'ribbits': ribbits, 'follow': True, })
    users = User.objects.all().annotate(ribbit_count=Count('ribbit'))
    ribbits = map(get_latest, users)
    obj = zip(users, ribbits)
    ribbit_form = ribbit_form or RibbitForm()
    return render(request,
                  'profiles.html',
                  {'obj': obj, 'next_url': '/users/',
                   'ribbit_form': ribbit_form,
                   'username': request.user.username, })
#Getting the latest giggle by each user is a bit tricky. We use Python's built in map() function for this and call get_latest() to all the elements of users queryset. The get_latest() function is defined in the code above and makes use of a backward relation on the User<-->Ribbit relation. For instance user.ribbit_set.all() would return all the giggles by the user. We order the giggles by id in descending order and slice the first element. The code is enclosed in a try catch block to catch the exception if no giggles are created by the user. We're then making use of Python's zip() function to link up each element of both iterators (users and giggles) so that we have a tuple with User Object and Latest giggle pair. We then pass along this zipped object along with the forms to the template. 
@login_required
def follow(request):
    if request.method == "POST":
        follow_id = request.POST.get('follow', False)
        if follow_id:
            try:
                user = User.objects.get(id=follow_id)
                request.user.profile.follows.add(user.profile)
            except ObjectDoesNotExist:
                return redirect('/users/')
    return redirect('/users/')
