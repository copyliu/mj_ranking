#-*- coding:utf-8 -*-
# Create your views here.


import mj_ranking.ranking.models as database
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required



def home(require):
    c={}
    Leagues=database.Leagues.objects.all()
    c["Leagues"]=Leagues
    return render_to_response("home.html",c)

def leagues(require,leagues):
    c={}
    r=database.Round.objects.filter(leagues=leagues).all()
    c["r"]=r
    return render_to_response("home.html",c)


