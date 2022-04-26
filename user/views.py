from django.contrib.sites import requests
from django.shortcuts import render, redirect
from user.exception import *
from django.contrib.auth import authenticate, login
from django.contrib import auth
from user.models import *
from django.http import HttpResponse, JsonResponse
from django.utils import timezone

import json
import os

import hashlib


def md5_generator(str):
    m = hashlib.md5()
    m.update(str.encode())
    return m.hexdigest()

# Create your views here.
def kakao_login(request):
    client_id = "06e362b49ca6cb8bbaff34b8b938a703"
    #redirect_uri = "https://ksnpick.com/users/login/kakao/callback/"
    redirect_uri = "http://localhost:8000/users/login/kakao/callback/"

    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )

def kakao_login_callback(request):
    code = request.GET.get("code", None)
    client_id = "06e362b49ca6cb8bbaff34b8b938a703"
    #redirect_uri = "https://ksnpick.com/users/login/kakao/callback/"
    redirect_uri = "http://localhost:8000/users/login/kakao/callback/"
    request_access_token = requests.post(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}",
        headers={"Accept": "application/json"},
    )



    access_token = request_access_token.json().get('access_token')
    refresh_token = request_access_token.json().get('refresh_token')
    user_info_response = requests.get('https://kapi.kakao.com/v2/user/me', headers={"Authorization" : f'Bearer ${access_token}'})

    profile_json = user_info_response.json()
    kakao_account = profile_json.get("kakao_account")
    profile = kakao_account.get("profile")

    id = profile_json.get("id")
    nickname = profile.get("nickname", None)
    email = kakao_account.get("email", None)
    gender = kakao_account.get("gender", None).upper()

    isKakao = User.objects.filter(snsId=id, snsType="카카오" )

    if( isKakao.count() <= 0 ) :
        # 계정이 있는 경우 로그인.
        nowTime = timezone.now()
        kakaoUser = User.objects.create(nickname=nickname, email=email, gender=gender, agreeUsage="1", agreePrivacy="1",
                                        accessToken=access_token, accessTokenExpireDate=nowTime, refreshToken=refresh_token,
                                        refreshTokenExpireDate=nowTime, deviceId="WEB", snsId=id, snsType="카카오",
                                        isApproved="0", isResign="0", isFirstLogin="1", isCertAdult="0", last_login=nowTime,
                                        regTime=nowTime, userType="NORMAL")

    kakao = User.objects.filter(snsId=id, snsType="카카오")

    # 회원가입 후에도 로그인 해야함.
    for row in kakao.values_list():
        userID = row[0]
        nickname = row[2]
        userType = row[14]

    setSession(request, userID, nickname, userType)
    updateLastVisit(userID)

    return redirect("/")


def localLogin (request) :
    if request.method == "GET" :
        return JsonResponse({"code": "1", "message" : "잘못된 접근입니다."})
    elif request.method == "POST" :
        username = request.POST['username']
        password = request.POST['password']

        pw = md5_generator(password)
        userIN = User.objects.filter(nickname=username, password=pw)

        if userIN.count() > 0 :
            for row in userIN.values_list():
                id = row[0]
                nickname = row[2]
                userType = row[14]

            setSession(request, id, nickname, userType)
            updateLastVisit(id)

            return JsonResponse({"code": "0"} )
        else :
            return JsonResponse({"code": "1", 'message' : "아이디 혹은 비밀번호가 일치 하지 않습니다."})
    else:
        return JsonResponse({"code": "1", "message" : "잘못된 접근입니다."})

def locallogout (request) :
    del request.session['nickName']
    del request.session['userType']

    return JsonResponse({"code": "0"} )

# 세션 생성.
def setSession(request, id, nickname, usertype) :
    request.session['id'] = id
    request.session['nickName'] = nickname
    request.session['userType'] = usertype
    request.session.set_expiry(0)
    return ""

def updateLastVisit(userID) :
    nowTime = timezone.now()
    updateTime = User.objects.filter(id = userID)
    updateTime.last_login = nowTime
    return ""