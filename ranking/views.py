#-*- coding:utf-8 -*-
# Create your views here.


import mj_ranking.ranking.models as database
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required


@login_required
def home(require):
    c={}
    Leagues=database.Leagues.objects.all()
    c["Leagues"]=Leagues
    render_to_response("home.html",c)
