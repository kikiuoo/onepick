import requests
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
import json
import os

from picktalk.models import *

import hashlib

#loginUrl = "https://ksnpick.com/users/login"
loginUrl = "http://localhost:8000/users/login"


def md5_generator(str):
    m = hashlib.md5()
    m.update(str.encode())
    return m.hexdigest()

# Create your views here.
def kakao_login(request):
    client_id = "fed078068136559dc83c4f5f40362e5f"
    redirect_uri = loginUrl + "/kakao/callback/"

    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )

def kakao_login_callback(request):
    code = request.GET.get("code", None)
    client_id = "fed078068136559dc83c4f5f40362e5f"
    redirect_uri = loginUrl + "/kakao/callback/"

    request_access_token = requests.post(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}",
        headers={"Accept": "application/json"},
    )

    access_token = request_access_token.json().get('access_token')
    user_info_response = requests.get('https://kapi.kakao.com/v2/user/me', headers={"Authorization" : f'Bearer ${access_token}'})

    profile_json = user_info_response.json()
    kakao_account = profile_json.get("kakao_account")
    profile = kakao_account.get("profile")

    id = str(profile_json.get("id"))
    email = kakao_account.get("email", None)

    isKakao = UserInfo.objects.filter( userid="kakao_"+id, jointype="KAKAO" )

    if( isKakao.count() <= 0 ) :
        # 계정이 있는 경우 로그인.
        nowTime = timezone.now()
        kakaoUser = UserInfo.objects.create(userid="kakao_"+id, email=email, jointype="KAKAO", regtime=nowTime, lastlogin=nowTime,
                                            logincount=1, usertype="NORMAL")

        key = str(UserInfo.objects.latest('num').num)

        return redirect("/users/join/"+key+"/")
    else :
        kakao = UserInfo.objects.filter(userid="kakao_"+id, jointype="KAKAO")

        for row in kakao.values_list():
            userID = row[1]
            userType = row[29]

        setSession(request, userID, userType)
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

    user_info_response = requests.get( "https://www.googleapis.com/oauth2/v3/userinfo",
        params={ 'access_token': access_token  }  )

    profile_json = user_info_response.json()

    sub = profile_json.get("sub")
    email = profile_json.get("email")

    isGoogle = UserInfo.objects.filter( userid="google_"+sub,  jointype="GOOGLE" )

    if( isGoogle.count() <= 0 ) :
        # 계정이 있는 경우 로그인.
        nowTime = timezone.now()
        googleUser = UserInfo.objects.create(userid="google_"+sub, email=email, jointype="GOOGLE", regtime=nowTime, lastlogin=nowTime,
                                            logincount=1, usertype="NORMAL")

        key = str(UserInfo.objects.latest('num').num)

        return redirect("/users/join/" + key + "/")

    else:
        google = UserInfo.objects.filter(userid="google_" + sub, jointype="GOOGLE")

        for row in google.values_list():
            userID = row[1]
            userType = row[29]

        setSession(request, userID, userType)
        updateLastVisit(userID)

        return redirect("/")



def localLogin (request) :
    if request.method == "GET" :
        return JsonResponse({"code": "1", "message" : "잘못된 접근입니다."})
    elif request.method == "POST" :
        username = request.POST['username']
        password = request.POST['password']


        pw = md5_generator(password)
        userIN = UserInfo.objects.filter(nickname=username, password=pw)

        """

        if userIN.count() > 0 :
            for row in userIN.values_list():
                userID = row[1]
                userType = row[29]

            setSession(request, id, nickname, userType)
            updateLastVisit(id)

            return JsonResponse({"code": "0"} )
        else :
            return JsonResponse({"code": "1", 'message' : "아이디 혹은 비밀번호가 일치 하지 않습니다."})
            
        """
    else:
        return JsonResponse({"code": "1", "message" : "잘못된 접근입니다."})

def locallogout (request) :
    del request.session['id']
    del request.session['userType']

    return JsonResponse({"code": "0"} )

# 세션 생성.
def setSession(request, id, usertype) :
    request.session['id'] = id
    request.session['userType'] = usertype
    request.session.set_expiry(0)

    return ""

def updateLastVisit(userID) :
    nowTime = timezone.now()

    updateTime = UserInfo.objects.get(userid = userID)
    updateTime.logincount = updateTime.logincount + 1
    updateTime.lastlogin = nowTime
    updateTime.save()

    insertLogin = UserLogin.objects.create(userid=userID)

    return ""



def join(request, num) :

    user = UserInfo.objects.get(num=num)
    userAgree = UserAgree.objects.filter(use="1").order_by("order")

    email = user.email.split('@')

    if user.birth != '' and user.birth != None :
        birth = user.birth.split('-')
    else :
        birth = ""

    if user.phone != '' and user.phone != None :
        phone = [user.phone[0:3], user.phone[3:7], user.phone[7:]]
    else :
        phone = ""

    return render(request, 'user/join.html', {'user': user, 'userAgree' : userAgree, 'email' : email, 'birth' : birth
                                              , 'phone' : phone})



def joinUpdate(request):

    num = request.POST['num']
    name = request.POST['name']
    phone1 = request.POST['phone1']
    phone2 = request.POST['phone2']
    phone3 = request.POST['phone3']
    email11 = request.POST['email1']
    email12 = request.POST['email12']
    brith1 = request.POST['brith1']
    brith2 = request.POST['brith2']
    brith3 = request.POST['brith3']
    birthType = request.POST['brithType']
    gender = request.POST['gender']
    agreeMail = request.POST["agreeMail"]

    updateUser = UserInfo.objects.get(num = int(num))
    updateUser.name = name
    updateUser.phone = phone1+phone2+phone3
    updateUser.email = email11 + "@" +email12
    updateUser.birth = brith1 + "-" + brith2 + "-" + brith3
    updateUser.birthType = birthType
    updateUser.gender = gender

    # 약관 동의
    updateUser.agreeusage = "1"
    updateUser.agreeprivacy = "1"
    updateUser.agreemarketing = "1"
    updateUser.agreeemail = agreeMail

    updateUser.save()

    return redirect("/")