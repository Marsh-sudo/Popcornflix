import email
import random
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
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth.forms import AuthenticationForm,SetPasswordForm
from .forms import RegisterUserForm,LoginUserForm,PasswordChangingForm
from .secrets import get_genres,get_movie,get_Nowplaying,get_trending,get_Toprated,get_video,get_popular,get_Upcoming


# Create your views here.
def register_request(request):
	if request.method == "POST":
		form = RegisterUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("login")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = RegisterUserForm()
	return render (request=request, template_name="register.html", context={"register_form":form})


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				print(user)
				return redirect("home")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form})

@login_required(login_url='password_change_view')
def password_change_view(request):
	if request.method == "POST":
		change_form = PasswordChangingForm(user=request.user,data=request.POST)
		if change_form.is_valid():
			change_form.save
			# password1 = change_form.cleaned_data["password1"]
			# password2 = change_form.cleaned_data["password2"]
			# if password1 == password2:
			# 	change_form.save()
			# user = change_form.save()
			# password_change(request,user)
			messages.success(request,"You have successfully changed your password!!")
			return redirect("password_confirm")
		messages.error(request,"Unsuccessful change")
	change_form = PasswordChangingForm(user=request.user)
	return render(request,"password/password_reset_confirm.html",{"change_form":change_form})

def password_confrim(request):
	return render(request,"password/password_reset_complete.html")

			   

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Request"
					email_template_name = "password/password_reset_email.txt"
					c = {
						"email":user.email,
						"domain":'127.0.0.1:8050',
						"site_name":"Popcornflix",
						"uid":user,
						"token":default_token_generator.make_token(user),
                        "protocol":"http",
					}
					email = render_to_string(email_template_name,c)
					try:
						send_mail(subject,email,'admin@example.com',[user.email],fail_silently=False)
						# return redirect("login")
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect("password_change_view")

	password_reset_form = PasswordResetForm()
	return render(request,"password/password_reset.html",{"password_reset_form":password_reset_form})


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
	return render(request,"rate.html",{"upcoming":upcoming['results']})

@login_required(login_url='login')
def Popular(request):
	popular = get_popular()
	return render(request,"popular.html",{"popularr":popular["results"]})

@login_required(login_url='login')
def Trending(request):
	trending = get_trending()
	return render(request,"trending.html",{"trending":trending["results"]})