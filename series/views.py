from django.shortcuts import render
from .siri import  get_airing_today,get_OnAir
# Create your views here.
def home_TV(request):
    On_Air = get_OnAir()
    airing_today = get_airing_today()

    return render(request,"TV.html",{"OnAir":On_Air,"today":airing_today})