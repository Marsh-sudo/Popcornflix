from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from movie.views import ProfileView

urlpatterns = [
    path('',views.home,name="home"),
    path("UserRegistration",views.register_request,name="UserRegistration"),
    path('login',views.login_request,name="login"),
    path("logout", views.logout_request, name= "logout"),
    path("play/<movie_id>",views.show_video,name="play"),
    path("upcoming",views.Upcoming,name="upcoming"),
    path("popular",views.Popular,name="popular"),
    path("trending",views.Trending,name="trending"),
    path("profile/",ProfileView.as_view(),name="profile"),
    path("Updateprofile",views.profile_update,name="Updateprofile")
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
