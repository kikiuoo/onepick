import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template import  loader
from django.db import connection

from picktalk.models import *
from django.conf import settings
from django.utils import timezone

from myonepick.common import *


def adminCheck(request):

    user = request.session.get('adminID', '')

    returnURL = "onepickAdmin/login/login.html"

    if user :
        returnURL = "onepickAdmin/main.html"

    return render( request, returnURL, {'pageType': "home" })


def adminLogin(request) :
    username = request.GET['username']
    password = request.GET['password']

    pw = md5_generator(password)
    userIN = UserInfo.objects.filter(userid=username, password=pw, usertype="admin")

    if userIN.count() > 0:
        userIN = UserInfo.objects.get(userid=username, password=pw, usertype="admin")

        request.session['adminID'] = userIN.userid
        request.session['adminName'] = userIN.name

        request.session.set_expiry(0)

        return JsonResponse({"code": "0"})
    else:
        return JsonResponse({"code": "1", 'message': "아이디 혹은 비밀번호가 일치 하지 않습니다."})



def adminLogout (request) :
    del request.session['adminID']
    #del request.session['adminName']

    return JsonResponse({"code": "0"} )