from sqlite3 import IntegrityError
from django.db import IntegrityError
from django.shortcuts import render_to_response,  render,RequestContext
from django.db.models import Q
from form import UserForm, UserProfileForm, Status_updateForm, Friendship_RequestForm, Friendship_AcceptForm,Rating_Form,LikeForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from models import Status_update,Friendship_Request
from django.contrib.auth.models import User
from models import UserProfile,Movie,Rating,Like,Comment
from friendship.models import Friend
from django.views import generic
from datetime import datetime
from math import *
from Recommendation_System.recommendations import *
from django.views.generic.edit import CreateView,UpdateView,DeleteView
# Create your views here.

class DetailView(generic.DetailView):
    model = Movie
    template_name = 'movie_detail.html'
    def get_context_data(self, **kwargs):
        context = super(DetailView,self).get_context_data(**kwargs)
        context['movie_details'] = Movie.objects.all()
        return context
class MovieCreate(generic.CreateView):
    model = Movie
    fields = ['title','year','director','writer','star_cast','imdb_ratings','genres','summary','length','movie_img','img']
    template_name = 'movie_form.html'
def index(request):
    return render_to_response('login.html',RequestContext(request))
@login_required
def accept_friendship(request):
    if request.method == 'POST':
        user_id = request.user.id
        req_f_fri = request.POST['r_f_f']
        req_t_fri = request.POST['r_t_f']
        friend = Friendship_Request.objects.filter(
            Q(request_from_friend=req_f_fri) & Q(request_to_friend=req_t_fri) & Q(friendship_status=0))
        print 'fri_req in accept friendship', friend
        for fr in friend:
            fr.friendship_status = 1
            fr.save()

    return render(request,'restricted.html',{})
@login_required
def movies(request):
    rated_moives = Rating.objects.all()
    try:
        if request.method == 'POST':

            ratin=float(request.POST['rate'])
            #get the rating from template
            mi= request.POST['movies_id']
            #get the movie id from template
            rate_movie = Rating_Form(data = request.POST)
            if rate_movie.is_valid() or 'rate_movie' in request.POST:
                rate = rate_movie.save(commit=False)
                rate.user = request.user
                #user set to the logged in user
                rate.movies_id = mi
                #set the movies_id of rating

                rate.rate = ratin
                #setting the rate of the movie
                rate.save()
            else:
                print rate_movie.errors
        else:
            rate_movie = Rating_Form()
    except IntegrityError:
        if request.method == 'POST':

            ratin=float(request.POST['rate'])
        new_rating = Rating.objects.get(movies_id=mi, user=request.user)
        print new_rating
        if new_rating:
            new_rating.rate = ratin
        new_rating.save()
    movies_name = Movie.objects.all()
    rated_moives = Rating.objects.all()
    new_rated = Rating.objects.all().filter( user=request.user)
    return render(request,'movies.html',{'rate_movie':rate_movie,'movies_name':movies_name,'rated_movies':rated_moives,'new_rated':new_rated})
def profile(request):
    profile_name = request.user.username
    print profile_name
    add_friend = User.objects.all()
    profile = request.user.id
    profile_pic = UserProfile.objects.all().filter(user_id = profile).order_by('id')
    status_user = request.user.id
    status_update_user = Status_update.objects.all().filter(posted_to_id=status_user).order_by('posted_by_id').reverse()

    return render(request,'profile.html',{'add_friend':add_friend,'profile_pic':profile_pic,'status_update_user':status_update_user,})
def rating(request,movie_id):
    if request.method == 'POST':
        rate_movie = Rating_Form(data = request.POST)
        if rate_movie.is_valid() or 'rate_movie' in request.POST:
            rate = rate_movie.save(commit=False)
            rate.save()
        else:
            print rate_movie.errors
    return render(request, 'movies.html', { 'rate_movie': rate_movie})
def friend_request_sending(request,id):
    if request.method == 'POST':
        r_t_f = request.POST['request_to_frnd']
        friend_request_form = Friendship_RequestForm(data=request.POST)
        user_id = request.user.id

        friend_request = friend_request_form.save(commit=False)
        friend_request.request_to_friend_id = r_t_f
        # request_to_friend = friend_request_form.cleaned_data['request_to_friend'].objects.all().exclude(request_to_friend=id)
        friend_request.request_from_friend_id = user_id
        friend_request.action_user = user_id

        friend_request.save()
    else:
        friend_request_form = Friendship_RequestForm()
    return render(request,'restricted.html',{'friendship_request_form':friend_request_form})
def status_update(request,id):
    likes_status = Like.objects.all()
    #getting the username of the passed parameter
    #user_name = User.objects.all().filter(id=id)

    status_user = id
    status_updated = False
    #if not request.user.is_staff or not request.user.is_superuser:
    #    raise Http404
    #if not request.user.is_authenticated():
    #    raise Http404
    if request.method == 'POST' and 'notif' in request.POST:

        username = request.user.username
        user_id = request.user.id
        status_update_form = Status_updateForm(data=request.POST)
        # pst_to = Status_update.objects.get(posted_to=id)
        status_form = status_update_form.save(commit=False)
        status_from_form = request.POST['status']
        status_form.posted_by_id = user_id
        status_form.posted_to_id = id
        status_form.status = status_from_form
        # if redirected to /restricted/ without passing id
        if status_form.posted_to_id is None:
            status_form.posted_to_id = user_id
            status_user = user_id
        status_form.save()

        status_updated = True
    if request.method == 'POST' and 'send_request' in request.POST:
        r_t_f = request.POST['request_to_frnd']
        friend_request_form = Friendship_RequestForm(data=request.POST)
        user_id = request.user.id

        friend_request = friend_request_form.save(commit=False)
        friend_request.request_to_friend_id = r_t_f
        # request_to_friend = friend_request_form.cleaned_data['request_to_friend'].objects.all().exclude(request_to_friend=id)
        friend_request.request_from_friend_id = user_id
        friend_request.action_user = user_id

        friend_request.save()
    else:
        friend_request_form = Friendship_RequestForm()
    '''if request.method == 'POST':


        if 'status_update_form' in request.POST and status_update_form.is_valid() :
            username = request.user.username
            user_id = request.user.id

            #pst_to = Status_update.objects.get(posted_to=id)
            status = status_update_form.save(commit=False)
            status.posted_by_id = user_id
            status.posted_to_id = id

            # if redirected to /restricted/ without passing id
            if status.posted_to_id is None:
                status.posted_to_id = user_id
                status_user=user_id
            status.save()

            status_updated=True
            print 'U r in status update form'

        elif  'friend_request_form' in request.POST and friend_request_form.is_valid():
            print 'U r in friend req form'
            user_id = request.user.id
            r_t_f = request.POST['request_to_frnd']
            friend_request = friend_request_form.save(commit=False)
            friend_request.request_to_form_id = r_t_f
            #request_to_friend = friend_request_form.cleaned_data['request_to_friend'].objects.all().exclude(request_to_friend=id)
            friend_request.request_from_friend_id = user_id
            friend_request.action_user = user_id
            friend_request.save()
        elif 'friend_acceform' in request.POST :
            print 'U r in friend accept form'
            user_id = request.user.id
            req_f_fri = request.POST['r_f_f']
            req_t_fri = request.POST['r_t_f']
            friend = Friendship_Request.objects.filter(Q(request_from_friend=req_f_fri) & Q(request_to_friend=req_t_fri) & Q(friendship_status=0))
            print 'fri_req',friend
            friend_accept_form = Friendship_AcceptForm(request.POST,instance=friend)
            friend_accept = friend_accept_form.save(commit=False)
            friend_accept.friendship_status = 1
            friend_accept.save()
        else:
            print status_update_form.errors,friend_request_form.errors
    else:

        friend_request_form = Friendship_RequestForm()
        friend_accept_form = Friendship_AcceptForm()'''
    #status_upadte_user = Status_update.objects.order_by('id').reverse()
    #status_user = request.user.id
    users = User.objects.all()
    profile_picture = UserProfile.objects.all().order_by('id')
    status_update_user = Status_update.objects.all().filter(posted_to_id=id).order_by('id').reverse()
    username_head = Status_update.objects.all().filter(posted_by_id=id)
    user_id = request.user.id
    friendlist = Friendship_Request.objects.filter((Q(request_to_friend = user_id)|Q(request_from_friend=user_id)) & Q(friendship_status=1))
    friend_list=[user_id]
    for friends in friendlist:
        if friends.request_from_friend_id == user_id:
            friend_list.append(friends.request_to_friend_id)
        if friends.request_to_friend_id == user_id:
            friend_list.append(friends.request_from_friend_id)
    friends_of_friends = {}
    f_o_f=[]
    for frined in friend_list:
        print frined
        friends_of_friends[frined] ={}
        print 'f',friends_of_friends
        f = Friendship_Request.objects.filter((Q(request_to_friend_id=frined)| Q(request_from_friend_id=frined)) & Q(friendship_status=1))
        fr = []
        for i in f:
            if i.request_from_friend_id == frined:
                fr.append(i.request_to_friend_id)
                f_o_f.append(i.request_to_friend_id)
            if i.request_to_friend_id == frined:
                fr.append(i.request_from_friend_id)
                f_o_f.append(i.request_from_friend_id)
        fr = list(set(fr))
        friends_of_friends[frined] = fr
    print 'friends',friends_of_friends
    print friend_list
    f_o_f = list(set(f_o_f))
    print 'f_o_f',f_o_f
    friend_suggestion = User.objects.filter(id__in=f_o_f)
    print 'friend_Sug',friend_suggestion
    '''status_update_user_friend = Status_update.objects.all()
    for stat in status_update_user_friend:
        if stat.posted_by_id in friend_list:
            print stat.posted_by_id'''
    status_update_user_friend_post = Status_update.objects.all().filter(posted_by_id__in= friend_list).order_by('created_on').reverse()


    print 'friend',friendlist
    for user in users:
        if user.pk not in friend_list:
            print user.username
    not_friend = User.objects.filter(username =friendlist)

    friend_rqst = Friendship_Request.objects.all().filter(Q(request_to_friend=user_id) & Q(friendship_status=0))
    nowhour = datetime.now().hour
    nowmin = datetime.now().minute
    status_user = [int(id)]
    rating = Rating.objects.all().filter()
    movies = {}
    for use in users:
        movies[use.username]={}
        rating = Rating.objects.all().filter(user=use.pk)
        for ratings in rating:
            movies[use.username][ratings.movies.title] = ratings.rate
    print movies
    rec= recommend(movies,request.user.username,sim_pearson)
    print rec
    recommended_movies = []
    all_movies = Movie.objects.all()
    for r in rec:
        for mov in all_movies:

            if mov.title == r[1]:
                recommended_movies.append(mov)
    print recommended_movies
    print status_user
    #username_heading = User.objects.all().filter(id=username_head)
    #print username_heading
    return render(request,'restricted.html',
                  {'friend_suggestion':friend_suggestion,'recommended_movies':recommended_movies,'likes_status':likes_status,'status_user':status_user,'nowhour':nowhour,'nowmin':nowmin,'profile_picture':profile_picture,'users':users,'friend_rqst':friend_rqst,'friend_request_form':friend_request_form,'username_head':username_head,'status_update_user_friend_post':status_update_user_friend_post,''''status_update_form': status_update_form,''' 'status_updated' : status_updated,'friend_list':friend_list },)

def news_feed(request,id):
    all_friend = Friendship_Request.objects.all().filter(Q(request_to_friend = id)|Q(request_from_friend=id),friendship_status=1)
    print all_friend
    return render(request,'news_feed.html',{'all_friend':all_friend})
def register(request):
    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False
    # If it's a HTTP POST, we're interested in processing form data
    if request.method == 'POST':

        # Attempt to grab information from the form information
        # Note that we make use of both UserForm and UserProfileForm

        user_form = UserForm(data=request.POST)
        user_profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid


        if user_form.is_valid() and user_profile_form.is_valid():
            # Save the user form data to database
            user = user_form.save()

            # Now we hash the password with the set_password method
            # Once hashed, we can update the user object

            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance
            # Since we need to set the user attribute ourselves, we set commit=False
            # This delays saving the model until we're ready to avoid integrity problems
            profile = user_profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            # Now we save the UserProfile model instance
            profile.save()

            # Update our variable to tell the template registration was successful
            registered=True

        # Invalid form or forms-mistakes or something else?
        # Print problems to the terminals
        # They will also be shown to the user
        else:
            print user_form.errors,user_profile_form.errors
    # Not a HTTP POST so we render our form using two ModelForm instances
    # These forms will be blank, ready for user input

    else:
        user_form = UserForm()
        user_profile_form = UserProfileForm()


    # Render the template depending on the context
    return render(request,
                  'registration.html',
                  {'user_form': user_form, 'user_profile_form': user_profile_form, 'registered': registered})



def user_login(request):
    # If the request is HTTP post try to pull out relevant information.
    if request.method == 'POST':
        # Gather username and password provided by the user.
        # This information is obtained from the login form.
            # We use request.POST.get('<variable>') as opposed to request.POST['<variable>']
            # because the request.POST.get('<variable>') returns none, if the value does not exists,
            # while the request.POST['<variable >'] will raise key error exception.
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django Machinary to attempt to see if the username/password
        # combination is valid - a user object is returned if it is.

        user = authenticate(username = username,password = password)
        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the acount active? It could have been disabled
            if user.is_active:
                '''user_id = User.objects.get(id)
                print id'''

                # If the account is valid and active, we can log the user in.
                # We will send the user back to homepage
                login(request,user)
                return HttpResponseRedirect('/movies/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse('Your account is disabled.')
        else:
            # Bad login details were provided. So we cant log the user in.
            print 'Invalid login details :{0},{1}'.format(username,password)
            return HttpResponse('Invalid login details supplied.')
        # The request is not a HTTP POST, so display the login form.
        # The scenario would most likely be a HTTP get.
    else:

# No context variables to pass to the template system, hence the
# blank dictionary object...
        return render(request,'login.html',{})
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def ajax_user_search(request):
    if request.method == 'POST':
        search_text = request.POST['search_text']
    else:
        search_text = ''

    results = Movie.objects.filter(title__contains = search_text)


    return render_to_response('ajax_search.html',{'results':results},context_instance = RequestContext( request ))
@login_required
def like(request):
    likes = Like.objects.all()
    if request.method=='POST':
        like_form = LikeForm(data=request.POST)
        like_status = request.POST['like_status']
        print like_status
        liked_by = request.POST['liked_by']
        like_f = like_form.save(commit=False)

        like_f.like_status_id = like_status
        like_f.liked_by_id = request.user.pk
        like_f.save()
        likes = Like.objects.all().filter(like_status=like_status)
    else:
        print 'Error'
    return render_to_response('ajax_like.html',{'likes':likes},context_instance = RequestContext( request ))
'''other_user =User.objects.get(pk=1)
Friend.objects.add_friend(
    request.user,
    other_user,
    message='Hi! I would like to add you.'
)'''
