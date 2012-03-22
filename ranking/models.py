#-*- coding:utf-8 -*-
from django.db import models

# Create your models here.


class Users(models.Model):
    jrm_id=models.CharField(max_length=20,null=True)
    tenhou_id=models.CharField(max_length=20,null=True)
    region=models.CharField(max_length=10,null=True)


class Leagues(models.Model):
    name=models.CharField(max_length=100,null=False)
    info=models.CharField(max_length=200,null=False)
    rule=models.TextField()

class Round(models.Model):
    leagues=models.ForeignKey(Leagues)
    name=models.CharField(max_length=100,null=False)

class Group(models.Model):
    round=models.ForeignKey(Round)
    name=models.CharField(max_length=100,null=False)

class Match(models.Model):
    group=models.ForeignKey(Group)
    name=models.CharField(max_length=100,null=False)

class Detail(models.Model):
    match=models.ForeignKey(Match)
    user=models.ForeignKey(Users)
    game=models.IntegerField(default=0)#對局數
    win=models.IntegerField(default=0)#和了
    lose=models.IntegerField(default=0)#放銃
    reach=models.IntegerField(default=0)#立直
    win_max=models.IntegerField(default=0)#最大和了點
    lose_max=models.IntegerField(default=0)#最大放銃點
    rank=models.IntegerField(default=0)#順位
    hulo=models.IntegerField(default=0)#副露次數
    end_point=models.IntegerField(default=0)#終局得點




