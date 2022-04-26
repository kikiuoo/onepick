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

loginUrl = "https://ksnpick.com/users/login"
#loginUrl = "http://localhost:8000/users/login"


def md5_generator(str):
    m = hashlib.md5()
    m.update(str.encode())
    return m.hexdigest()

# Create your views here.
def kakao_login(request):
    client_id = "06e362b49ca6cb8bbaff34b8b938a703"
    redirect_uri = loginUrl + "/kakao/callback/"

    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )

def kakao_login_callback(request):
    code = request.GET.get("code", None)
    client_id = "06e362b49ca6cb8bbaff34b8b938a703"
    redirect_uri = loginUrl + "/kakao/callback/"
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


# 구글 로그인 API 호출
def googleLogin(request):
    app_key = "823806029358-6tgcgl07h192l7dcsbi6va1jp0lphnne.apps.googleusercontent.com"
    scope = "https://www.googleapis.com/auth/userinfo.email " + \
            "https://www.googleapis.com/auth/userinfo.profile"

    redirect_uri = loginUrl + "/google/callback/"
    google_auth_api = "https://accounts.google.com/o/oauth2/v2/auth"

    response = redirect(
        f"{google_auth_api}?client_id={app_key}&response_type=code&redirect_uri={redirect_uri}&scope={scope}"
    )

    return response


# 구글 로그인 처리.
def googleLoginCallback(request):
    code = request.GET.get('code')
    client_id = "823806029358-6tgcgl07h192l7dcsbi6va1jp0lphnne.apps.googleusercontent.com"
    client_secret = "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"

    redirection_uri = loginUrl + "/google/callback/"
    grant_type = 'authorization_code'
    state = "random_string"

    request_access_token = requests.post(
         f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type={grant_type}&redirect_uri={redirection_uri}&state={state}"
    )

    access_token = request_access_token.json().get('access_token')
    id_token = request_access_token.json().get('id_token')

    user_info_response = requests.get( "https://www.googleapis.com/oauth2/v3/userinfo",
        params={ 'access_token': access_token  }  )

    profile_json = user_info_response.json()

    sub = profile_json.get("sub")
    nickname = profile_json.get("sub")
    email = profile_json.get("sub")

    isGoogle = User.objects.filter( snsId=sub, snsType="구글" )

    if( isGoogle.count() <= 0 ) :
        # 계정이 있는 경우 로그인.
        nowTime = timezone.now()
        googleUser = User.objects.create(nickname=nickname, email=email, agreeUsage="1", agreePrivacy="1",
                                        accessToken=access_token, accessTokenExpireDate=nowTime, refreshToken=id_token,
                                        refreshTokenExpireDate=nowTime, deviceId="WEB", snsId=sub, snsType="구글",
                                        isApproved="0", isResign="0", isFirstLogin="1", isCertAdult="0", last_login=nowTime,
                                        regTime=nowTime, userType="NORMAL")

    google = User.objects.filter(snsId=sub, snsType="구글")

    # 회원가입 후에도 로그인 해야함.
    for row in google.values_list():
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