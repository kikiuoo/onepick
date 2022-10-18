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

    face = ProfileImgclass.objects.filter(subcate='얼굴형').order_by("imgclass")
    body = ProfileImgclass.objects.filter(subcate='체형').order_by("imgclass")
    img = ProfileImgclass.objects.filter(subcate='이미지').order_by("imgclass")
    job = ProfileImgclass.objects.filter(subcate='직업').order_by("imgclass")

    return render( request, urlBase + "index.html",
                   { 'pageType': "classfy", "profileInfo" : profileInfo, "face": face,
                     "body": body, "img": img, "job": job })



def saveClassfy(request):

    saveChk_face = request.GET.get("saveChk_face", "")
    saveChk_body = request.GET.get("saveChk_body", "")
    saveChk_img = request.GET.get("saveChk_img", "")
    saveChk_job = request.GET.get("saveChk_job", "")
    profileNum = request.GET.get("profileNum", "")

    profileInfo = ProfileInfo.objects.get(num=profileNum)
    if profileInfo.classface == "" or profileInfo.classface == None :
        profileInfo.classface = saveChk_face
    else :
        profileInfo.classface = profileInfo.classface + "," + saveChk_face

    if profileInfo.classbody == "" or profileInfo.classbody == None :
        profileInfo.classbody = saveChk_body
    else :
        profileInfo.classbody = profileInfo.classbody + "," + saveChk_body


    if profileInfo.classimg == "" or profileInfo.classimg == None :
        profileInfo.classimg = saveChk_img
    else :
        profileInfo.classimg = profileInfo.classimg + "," + saveChk_img


    if profileInfo.classjob == "" or profileInfo.classjob == None :
        profileInfo.classjob = saveChk_job
    else :
        profileInfo.classjob = profileInfo.classjob + "," + saveChk_job

    profileInfo.clsscount = profileInfo.clsscount + 1

    profileInfo.save()

    return JsonResponse({"code": "0"})
