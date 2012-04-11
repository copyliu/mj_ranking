# -*- coding: utf-8 -*-
# Create your views here.
from django.db.models.query import QuerySet
from django.shortcuts import render_to_response
from django.db.models import *
import mj_ranking.ranking.models as database
import django.shortcuts
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.utils.simplejson import dumps, loads, JSONEncoder
from django.db import models

class DjangoJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, QuerySet):
            # `default` must return a python serializable
            # structure, the easiest way is to load the JSON
            # string produced by `serialize` and return it
            return loads(serialize('json', obj))
        if isinstance(obj, models.Model):
            return dict([(attr, getattr(obj, attr)) for attr in [f.name for f in obj._meta.fields]])
        return JSONEncoder.default(self, obj)


#'{callback}({json})'.format(callback=request.GET['callback'], json=MyJSON)
def home(request):
    c = {}
    Leagues = database.Leagues.objects.all()
    c["Leagues"] = Leagues
    return django.shortcuts.render_to_response("home.html", c)


@login_required
def inputresult(request):
    c = {}
    if request.method == "GET":
        Leagues = database.Leagues.objects.all()
        c["Leagues"] = Leagues
        return django.shortcuts.render_to_response('inputresult.html', c)
    elif request.method == "POST":
        returninfo = {"error": 0, "msg": u"保存成功"}

        if request.POST.get("type", "") and request.POST.get("match", ""):
            #只會有ajax啦
            match = database.Match.objects.get(id=int(request.POST["match"]))
            lines = request.POST.get("value", "").splitlines()

            if not lines:
                returninfo["error"] = -1
                returninfo["msg"] = u"沒有收到任何數據"

                MyJSON = dumps(returninfo)#,cls=DjangoJSONEncoder)
                return django.shortcuts.HttpResponse(MyJSON,
                    mimetype="application/json")
            if database.Detail.objects.filter(match=match).count()>0:
                returninfo["error"] = -1
                returninfo["msg"] = u"該場已有數據"

                MyJSON = dumps(returninfo)#,cls=DjangoJSONEncoder)
                return django.shortcuts.HttpResponse(MyJSON,
                    mimetype="application/json")
            if not 2 < len(lines) < 5:
                returninfo["error"] = -1
                returninfo["msg"] = u"參與人數不正確"

                MyJSON = dumps(returninfo)#,cls=DjangoJSONEncoder)
                return django.shortcuts.HttpResponse(MyJSON,
                    mimetype="application/json")
            ModelsDT = []
            for l in lines:
                datas = l.split("|")

                #名字|对局数|和了|放铳|立直|最高和了|最高放铳|顺位|最终点数|副露|对局名
                if len(datas) < 10:
                    returninfo["error"] = -1
                    returninfo["msg"] = u"數據不完整"
                    MyJSON = dumps(returninfo)#,cls=DjangoJSONEncoder)
                    return django.shortcuts.HttpResponse(MyJSON, mimetype="application/json")
                MatchUser = database.Users.objects.filter(jrm_id=datas[0]).all()
                if not len(MatchUser):
                    returninfo["error"] = -1
                    returninfo["msg"] = u"參賽者 : " + datas[0] + u" 不存在, 請檢查名字或到後臺添加"
                    MyJSON = dumps(returninfo)#,cls=DjangoJSONEncoder)
                    return django.shortcuts.HttpResponse(MyJSON, mimetype="application/json")
                    #名字|对局数|和了|放铳|立直|最高和了|最高放铳|顺位|最终点数|副露|对局名
                try:
                    d = database.Detail()
                    d.match = match
                    d.user = MatchUser[0]
                    d.game = int(datas[1])
                    d.win = int(datas[2])
                    d.lose = int(datas[3])
                    d.reach = int(datas[4])
                    d.win_max = int(datas[5])
                    d.lose_max = int(datas[6])
                    d.rank = int(datas[7])
                    d.end_point = int(datas[8])
                    d.hulo = int(datas[9])
                    ModelsDT.append(d)
                except:
                    returninfo["error"] = -1
                    returninfo["msg"] = u"數據格式錯誤"
                    MyJSON = dumps(returninfo)#,cls=DjangoJSONEncoder)
                    return django.shortcuts.HttpResponse(MyJSON, mimetype="application/json")
            for i in ModelsDT:
                i.save()
            MyJSON = dumps(returninfo)#,cls=DjangoJSONEncoder)
            return django.shortcuts.HttpResponse(MyJSON, mimetype="application/json")
        else:
            return django.shortcuts.HttpResponse("")



def JsonData(request):
    callback = request.GET.get("callback", "")
    returninfo = {}
    if request.GET.get("show_round", ""):
        #SHOW_ROUND
        lid = int(request.GET["show_round"])
        league = database.Leagues.objects.get(id=lid)
        rounds = database.Round.objects.filter(leagues=league).all()
        returninfo["leagues"] = league
        returninfo["rounds"] = rounds
        MyJSON = dumps(returninfo, cls=DjangoJSONEncoder)
        return django.shortcuts.HttpResponse('%s(%s)'%(request.GET['callback'],MyJSON),
            mimetype="application/json")
    if request.GET.get("show_group", ""):
        #SHOW GROUP
        gid = int(request.GET["show_group"])
        round = database.Round.objects.get(id=gid)
        groups = database.Group.objects.filter(round=round).all()
        returninfo["round"] = round
        returninfo["groups"] = groups
        MyJSON = dumps(returninfo, cls=DjangoJSONEncoder)
        return django.shortcuts.HttpResponse('%s(%s)'%(request.GET['callback'],MyJSON),
            mimetype="application/json")

    if request.GET.get("show_match", ""):
        #SHOW GROUP
        gid = int(request.GET["show_match"])
        group = database.Group.objects.get(id=gid)
        matchs = database.Match.objects.filter(group=group).all()
        returninfo["group"] = group
        returninfo["matchs"] = matchs
        MyJSON = dumps(returninfo, cls=DjangoJSONEncoder)
        return django.shortcuts.HttpResponse('%s(%s)'%(request.GET['callback'],MyJSON),
            mimetype="application/json")


def viewleague(request, p1):
    c = {}
    League = database.Leagues.objects.get(pk=p1)
    c["League"] = League
    return render_to_response('viewleague.html' ,c)


def getJSONv2(request):
    if request.GET.get("lid", ""):
        lid = int(request.GET["lid"])

        League= database.Leagues.objects.get(pk=lid)
        alluser=database.Users.objects.filter(detail__match__group__round__leagues__id=1).distinct()
        alldetail=database.Detail.objects.filter(match__group__round__leagues__id=lid).select_related()
        result=[]
        for u in alluser:

#
#            hulo=alldetail.filter(user=u).aggregate(agg=Sum("hulo"))["agg"]
#            game=alldetail.filter(user=u).aggregate(agg=Sum("game"))["agg"]
#            lose=alldetail.filter(user=u).aggregate(agg=Sum("lose"))["agg"]
#            lose_max=max([ abs(i["lose_max"]) for i in alldetail.filter(user=u).values("lose_max") ])
#            end_point=alldetail.filter(user=u).aggregate(agg=Avg("end_point"))["agg"]
#            rank=alldetail.filter(user=u).aggregate(agg=Avg("rank"))["agg"]
#            reach=alldetail.filter(user=u).aggregate(agg=Sum("reach"))["agg"]
#            win=alldetail.filter(user=u).aggregate(agg=Sum("win"))["agg"]
#            win_max=alldetail.filter(user=u).aggregate(agg=Max("win_max"))["agg"]

            udetail=alldetail.filter(user=u).select_related()
            hulo=sum([ abs(i.hulo) for i in udetail ])
            game=sum([ abs(i.game) for i in udetail ])
            lose=sum([ abs(i.lose) for i in udetail ])
            lose_max=max([ abs(i.lose_max) for i in udetail ])
            end_point=round(float(sum([ i.end_point for i in udetail ]))/udetail.count(),2)
            rank=round(float(sum([ i.rank for i in udetail ]))/udetail.count(),2)
            reach=sum([ abs(i.reach) for i in udetail ])
            win=sum([ abs(i.win) for i in udetail ])
            win_max=max([ abs(i.win_max) for i in udetail ])

            rank1=[ i.rank for i in udetail ].count(1)
            rank2=[ i.rank for i in udetail ].count(2)
            rank3=[ i.rank for i in udetail ].count(3)
            rank4=[ i.rank for i in udetail ].count(4)
            result.append({
                "jrm_id":u.jrm_id,
                "hulo":hulo,
                "game":game,
                            "lose":lose,
                            "lose_max":lose_max,
                            "end_point":end_point,
                            "rank":rank,
                            "reach":reach,
                            "win":win,
                            "win_max":win_max,
                            "rank1":rank1,
                            "rank2":rank2,
                            "rank3":rank3,
                            "rank4":rank4,

                            })
        webreturn={"result":result}
        MyJSON = dumps(result, cls=DjangoJSONEncoder)
        return django.shortcuts.HttpResponse(MyJSON)