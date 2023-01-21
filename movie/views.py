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
from django.contrib.auth.views import PasswordChangeView,LoginView,PasswordResetView
from django.views.generic import DetailView,ListView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from .forms import UpdateProfileForm,UpdateUserForm,PasswordChangingForm,LoginForm,RegisterForm,SignUpForm
from .secrets import get_genres,get_movie,get_Nowplaying,get_trending,get_Toprated,get_video,get_popular,get_Upcoming
from .models import Profile

# Create your views here.
class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})

class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)

# def register_request(request):
# 	if request.method == "POST":
# 		form = SignUpForm(request.POST)
# 		if form.is_valid():
# 			user = form.save()
# 			user.save()
# 			login(request, user)
# 			print(user)
# 			messages.success(request, "Registration successful." )
# 			return redirect("login")
# 		messages.error(request, "Unsuccessful registration. Invalid information.")
# 	form = SignUpForm()
# 	return render (request=request, template_name="register.html", context={"register_form":form})


# def login_request(request):
# 	if request.method == "POST":
# 		username = request.POST.get('username')
# 		password = request.POST.get('password')
# 		user = authenticate(request,username=username,password=password)
# 		print(username)
# 		print(password)
# 		if user and user.is_active==False:
# 			login(request,user)
# 			print(user)
# 			return redirect("home")
# 		else:
# 			messages.success(request,"Sorry there was an error login In!! Try again...")
# 			return redirect("login")

# 	else:
# 		return render(request,"login.html",{})
   
	


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

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'password/password_reset.html'
    email_template_name = 'password/password_reset_email.html'
    subject_template_name = 'password/password_reset_subject.html'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('home')