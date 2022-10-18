from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template import  loader
from django.db import connection

from picktalk.models import *
from django.db.models import Q
from django.utils import timezone

from myonepick.common import *


urlBase = "onepickAdmin/classfy/"


def classfy(request):

    profileInfo = ProfileInfo.objects.filter(clsscount=0).order_by('?')[:1]

    imgClass = ProfileImgclass.objects.all().order_by("imgclass")

    return render( request, urlBase + "index.html",
                   { 'pageType': "classfy", "profileInfo" : profileInfo, "imgClass": imgClass })



def saveClassfy(request):

    #saveChk": saveChk , "profileNum" : profileNum
    saveChk = request.GET.get("saveChk", "")
    profileNum = request.GET.get("profileNum", "")

    profileInfo = ProfileInfo.objects.get(num=profileNum)
    if profileInfo.classtag == "" or profileInfo.classtag == None :
        profileInfo.classtag = saveChk
    else :
        profileInfo.classtag = profileInfo.classtag + "," + saveChk

    profileInfo.clsscount = profileInfo.clsscount + 1

    profileInfo.save()

    return JsonResponse({"code": "0"})
