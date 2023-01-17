import email
import random
import requests
from django.shortcuts import render,redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail,BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.views.generic import DetailView,ListView
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth.forms import AuthenticationForm,SetPasswordForm
from .forms import SignUpForm,UpdateProfileForm,UpdateUserForm,PasswordChangingForm
from .secrets import get_genres,get_movie,get_Nowplaying,get_trending,get_Toprated,get_video,get_popular,get_Upcoming
from .models import Profile,Users

# Create your views here.
def register_request(request):
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			print(user)
			messages.success(request, "Registration successful." )
			return redirect("login")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = SignUpForm()
	return render (request=request, template_name="register.html", context={"register_form":form})


def login_request(request):
	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request,username=username,password=password)
		print(username)
		print(password)
		print(dir(user))
		if user:
			login(request,user)
			print(user)
			return redirect("home")
		else:
			messages.success(request,"Sorry there was an error logging In!! Try again...")
			return redirect("login")

	else:
		return render(request,"login.html",{})


@login_required(login_url='login')
def home(request):
	#logic for types of movies
	movie = get_trending()
	random_movies = random.randrange(0,18)
	poster = movie['results'][random_movies]
	trending = movie['results']
	top_rated = get_Toprated()
	upcoming_movie = get_Upcoming()
	
	#action movies
	action = get_genres(28)
	

	#animation movies
	anime = get_genres(16)

	#comegy movies
	comedy_movie = get_genres(35)

	#horror
	horror = get_genres(27)

	#documentary
	documentary = get_genres(99)

	#adventure
	adventure = get_genres(12)

	#fantasy
	fantasy = get_genres(14)

	#thrillers
	thriller = get_genres(53)

	#science fiction
	fictions = get_genres(878)

	popular = get_popular()

	return render(request,'home.html',{
		"poster":poster,
		"trending":trending,
		"popular":popular["results"],
		"Upcoming":upcoming_movie["results"],
		"action":action['items'],
		"horror":horror['items'],
		"comedy":comedy_movie['items'],
		"fantasy":fantasy['items'],
		"adventure":adventure['items'],
		"thriller":thriller['items'],
		"fictions":fictions['items'],
		"TopRated":top_rated['results'],
		"documentary":documentary['items'],
		"anime":anime['items'],
	})

@login_required(login_url='login')
def show_video(request,movie_id):
	video = get_video(movie_id)
	video_info = video['results'][0]
	youtube_url = f"www.youtube.com/watch?v={video_info['key']}"

	return render(request,'play.html',{'url':youtube_url})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("login")

@login_required(login_url='login')
def Upcoming(request):
	upcoming = get_Upcoming()
	return render(request,"upcoming.html",{"upcoming":upcoming['results']})

@login_required(login_url='login')
def Popular(request):
	popular = get_popular()
	return render(request,"popular.html",{"popularr":popular["results"]})

@login_required
def Trending(request):
	trending = get_trending()
	return render(request,"trending.html",{"trending":trending["results"]})



def profile_update(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'profile-update.html', {'user_form': user_form, 'profile_form': profile_form})


class ProfileView(ListView):
	model = Profile
	template_name = "profile.html"