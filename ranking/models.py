#-*- coding:utf-8 -*-
from django.db import models
from django.contrib import admin
# Create your models here.


class Users(models.Model):
    jrm_id=models.CharField(max_length=20,null=True,verbose_name="雀龍門ID")
    tenhou_id=models.CharField(max_length=20,null=True,verbose_name="天鳳名字")
    region=models.CharField(max_length=10,null=True,verbose_name="來自")

    class Meta:
        verbose_name_plural=verbose_name = "選手"
    def __unicode__(self):
        return u"雀龍門: %s, 天鳳: %s"%(self.jrm_id,self.tenhou_id)

class Leagues(models.Model):
    name=models.CharField(max_length=100,null=False,verbose_name="名稱")
    info=models.CharField(max_length=200,null=False,verbose_name="簡介")
    rule=models.TextField(verbose_name="規則說明")
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural=verbose_name="聯賽"


class Round(models.Model):
    leagues=models.ForeignKey(Leagues,verbose_name="聯賽名")
    name=models.CharField(max_length=100,null=False,verbose_name="名稱")
    def __unicode__(self):
        return self.leagues.name+self.name
    class Meta:
        verbose_name_plural=verbose_name="輪次"
class RoundAdmin(admin.ModelAdmin):
    list_display = ('name','leagues')
    list_filter = ("leagues", )

class Group(models.Model):
    round=models.ForeignKey(Round,verbose_name="輪次")
    name=models.CharField(max_length=100,null=False,verbose_name="組名")
    class Meta:
        verbose_name_plural=verbose_name="分組"
    def get_leagues(self):
        return self.round.leagues
    get_leagues.short_description="聯賽名"
    def __unicode__(self):
        return self.round.leagues.name+self.round.name+self.name

class GroupAdmin(admin.ModelAdmin):
    list_display = ('name','round')
    list_filter = ( "round__leagues",)

class Match(models.Model):
    group=models.ForeignKey(Group,verbose_name="小組")
    name=models.CharField(max_length=100,null=False,verbose_name="場次")
    class Meta:
        verbose_name_plural=verbose_name="場次"
    def __unicode__(self):
        return self.group.round.leagues.name+self.group.round.name+self.group.name+self.name
class MatchAdmin(admin.ModelAdmin):
    list_display = ("name","group")
    list_filter = ( "group__round__leagues","group__round")
class Detail(models.Model):
    match=models.ForeignKey(Match,verbose_name="場次")
    user=models.ForeignKey(Users,verbose_name="選手")
    game=models.IntegerField(default=0,verbose_name="對局數")#對局數
    win=models.IntegerField(default=0,verbose_name="和了數")#和了
    lose=models.IntegerField(default=0,verbose_name="放銃數")#放銃
    reach=models.IntegerField(default=0,verbose_name="立直數")#立直
    win_max=models.IntegerField(default=0,verbose_name="最大和了點")#最大和了點
    lose_max=models.IntegerField(default=0,verbose_name="最大放銃點")#最大放銃點
    rank=models.IntegerField(default=0,verbose_name="順位")#順位
    hulo=models.IntegerField(default=0,verbose_name="副露次數")#副露次數
    end_point=models.IntegerField(default=0,verbose_name="終局得點")#終局得點
    class Meta:
        verbose_name_plural=verbose_name="對局情報"
    def __unicode__(self):
        return self.match.group.round.leagues.name+self.match.group.round.name+self.match.group.name+self.match.name+self.match.name+u": "+unicode(self.user)
class DetailAdmin(admin.ModelAdmin):
    list_display = ("user","match")
    list_filter = ( "match__group__round__leagues","match__group__round")


