from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('',views.home,name="home"),
    path('register',views.register_request,name="register"),
    path('login',views.login_request,name="login"),
    path("logout", views.logout_request, name= "logout"),
    path("play/<movie_id>",views.show_video,name="play"),
    path("upcoming",views.Upcoming,name="upcoming"),
    path("popular",views.Popular,name="popular"),
    path("trending",views.Trending,name="trending"),
    path("password_change_view",views.password_change_view,name="password_change_view"),
    path("password_confirm",views.password_confrim,name="password_confirm"),
    path("password_reset", views.password_reset_request, name="password_reset"),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
