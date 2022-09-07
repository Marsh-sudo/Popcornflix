from django.urls import path
from . import views

urlpatterns = [
    path("streams",views.home_TV,name="series"),
    
    
]