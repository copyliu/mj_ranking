#-*- coding:utf-8 -*-
# Create your views here.
from django.db.models.query import QuerySet

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
        returninfo = {"error": 0, "msg": "保存成功"}

        if request.POST.get("type", "") and request.POST.get("match", ""):
            #只會有ajax啦
            match = database.Match.objects.get(id=int(request.POST["match"]))
            lines = request.POST.get("value", "").splitlines()

            if not lines:
                returninfo["error"] = -1
                returninfo["msg"] = "沒有收到任何數據"

                MyJSON = dumps(returninfo)#,cls=DjangoJSONEncoder)
                return django.shortcuts.HttpResponse(MyJSON,
                    mimetype="application/json")
            if database.Detail.objects.filter(match=match).count()>0:
                returninfo["error"] = -1
                returninfo["msg"] = "該場已有數據"

                MyJSON = dumps(returninfo)#,cls=DjangoJSONEncoder)
                return django.shortcuts.HttpResponse(MyJSON,
                    mimetype="application/json")
            if not 2 < len(lines) < 5:
                returninfo["error"] = -1
                returninfo["msg"] = "參與人數不正確"

                MyJSON = dumps(returninfo)#,cls=DjangoJSONEncoder)
                return django.shortcuts.HttpResponse(MyJSON,
                    mimetype="application/json")
            ModelsDT = []
            for l in lines:
                datas = l.split("|")

                #名字|对局数|和了|放铳|立直|最高和了|最高放铳|顺位|最终点数|副露|对局名
                if len(datas) < 10:
                    returninfo["error"] = -1
                    returninfo["msg"] = "數據不完整"
                    MyJSON = dumps(returninfo)#,cls=DjangoJSONEncoder)
                    return django.shortcuts.HttpResponse(MyJSON, mimetype="application/json")
                MatchUser = database.Users.objects.filter(jrm_id=datas[0]).all()
                if not len(MatchUser):
                    returninfo["error"] = -1
                    returninfo["msg"] = "參賽者 : " + datas[0] + " 不存在, 請檢查名字或到後臺添加"
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
                    returninfo["msg"] = "數據格式錯誤"
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
        return django.shortcuts.HttpResponse('{callback}({json})'.format(callback=request.GET['callback'], json=MyJSON),
            mimetype="application/json")
    if request.GET.get("show_group", ""):
        #SHOW GROUP
        gid = int(request.GET["show_group"])
        round = database.Round.objects.get(id=gid)
        groups = database.Group.objects.filter(round=round).all()
        returninfo["round"] = round
        returninfo["groups"] = groups
        MyJSON = dumps(returninfo, cls=DjangoJSONEncoder)
        return django.shortcuts.HttpResponse('{callback}({json})'.format(callback=request.GET['callback'], json=MyJSON),
            mimetype="application/json")

    if request.GET.get("show_match", ""):
        #SHOW GROUP
        gid = int(request.GET["show_match"])
        group = database.Group.objects.get(id=gid)
        matchs = database.Match.objects.filter(group=group).all()
        returninfo["group"] = group
        returninfo["matchs"] = matchs
        MyJSON = dumps(returninfo, cls=DjangoJSONEncoder)
        return django.shortcuts.HttpResponse('{callback}({json})'.format(callback=request.GET['callback'], json=MyJSON),
            mimetype="application/json")

