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

    id = str(profile_json.get("id"))
    email = kakao_account.get("email", None)

    returnUrl = userLogin(request, "google_"+id, email, "", "", "", "KAKAO")

    return redirect(returnUrl)




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

    returnUrl = userLogin(request, "google_"+sub, email, "", "", "", "GOOGLE")

    return redirect(returnUrl)


def naver_login(request):
    client_id = "0HGf7pdIAXwsh0Jvwa6_"
    redirect_uri = loginUrl + "/naver/callback/"

    print(f"https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&state=RAMDOM_STATE")
    return redirect(
        f"https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&state=RAMDOM_STATE"
    )

def naver_login_callback(request):
    code = request.GET.get("code", None)
    state = request.GET.get("state", None)
    client_id = "0HGf7pdIAXwsh0Jvwa6_"
    client_secret = "_5rS6cXipg"
    redirect_uri = loginUrl + "/naver/callback/"

    request_access_token = requests.post(
        f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&redirect_uri={redirect_uri}&code={code}&state={state}",
        headers={"Accept": "application/json"},
    )

    access_token = request_access_token.json().get('access_token')
    user_info_response = requests.get('https://openapi.naver.com/v1/nid/me?token_type=access_token&access_token='+access_token)

    profile_json = user_info_response.json()
    response = profile_json.get("response")

    id = response.get("id")
    email = response.get("email", None)
    gender = response.get("gender", None)
    name = response.get("name", None)
    birthday = response.get("birthday", None)
    birthyear = response.get("birthyear", None)

    returnUrl = userLogin(request, "naver_"+id, email, gender, name, birthyear+"-"+birthday, "NAVER")

    return redirect(returnUrl)


def localLogin (request) :

    return render(request, 'user/login.html')

def localLoginCallback (request) :
    if request.method == "GET" :
        return JsonResponse({"code": "1", "message" : "잘못된 접근입니다."})
    elif request.method == "POST" :
        username = request.POST['username']
        password = request.POST['password']


        pw = md5_generator(password)
        userIN = UserInfo.objects.filter(userid=username, password=pw)

        if userIN.count() > 0 :
            userIN = UserInfo.objects.get(userid=username, password=pw)

            request.session['id'] = userIN.userid
            request.session['userType'] = userIN.usertype
            request.session.set_expiry(0)

            updateLastVisit(userIN.userid)

            return JsonResponse({"code": "0"} )
        else :
            return JsonResponse({"code": "1", 'message' : "아이디 혹은 비밀번호가 일치 하지 않습니다."})

    else:
        return JsonResponse({"code": "1", "message": "잘못된 접근입니다."})


def userLogin(request, id, email, gender, name, birth, joinType) :

    returnUrl = ""
    isUser = UserInfo.objects.filter(userid=id, jointype=joinType)

    if isUser.count() <= 0 :
        nowTime = timezone.now()
        addUser = UserInfo.objects.create(userid=id, email=email, jointype=joinType, gender=gender, name=name,
                                          birth=birth, regtime=nowTime, lastlogin=nowTime, logincount=1,
                                          usertype="NORMAL")
        key = addUser.userid

        returnUrl = "/users/join/" + str(key) + "/social/"
    else :
        isUser = UserInfo.objects.get(userid=id, jointype=joinType)

        userID = isUser.userid
        userType = isUser.usertype

        request.session['id'] = userID
        request.session['userType'] = userType
        request.session.set_expiry(0)

        updateLastVisit(userID)

        returnUrl = "/"
    return returnUrl


def locallogout (request) :
    del request.session['id']
    del request.session['userType']

    return JsonResponse({"code": "0"} )


def updateLastVisit(userID) :
    nowTime = timezone.now()

    updateTime = UserInfo.objects.get(userid = userID)
    updateTime.logincount = updateTime.logincount + 1
    updateTime.lastlogin = nowTime
    updateTime.save()

    insertLogin = UserLogin.objects.create(userid=userID, accesstime=nowTime)

    return ""

def joinView(request) :

    return render(request, 'user/joinView.html')


# 회원가입.
def join(request, userID, type) :
    user = UserInfo.objects.get(userid=userID)

    return render(request, 'user/join.html', {'user': user, 'type': type})



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



# id, pw 찾기
def finduser(request) :

    return render(request, 'user/findUser.html')

def findPW (request) :
    if request.method == "GET" :
        return JsonResponse({"code": "1", "message" : "잘못된 접근입니다."})
    elif request.method == "POST" :
        userID = request.POST['userID']
        userName = request.POST['userName']

        userIN = UserInfo.objects.filter(userid=userID, name=userName)

        if userIN.count() > 0 :
            return JsonResponse({"code": "0"} )
        else :
            return JsonResponse({"code": "1", 'message' : "아이디와 이름이 일치하는 정보가 없습니다."})

    else:
        return JsonResponse({"code": "1", "message": "잘못된 접근입니다."})

def updatePW(request) :
    if request.method == "GET" :
        return JsonResponse({"code": "1", "message" : "잘못된 접근입니다."})
    elif request.method == "POST" :
        userID = request.POST['userID']
        password = request.POST['password']

        userIN = UserInfo.objects.get(userid=userID)
        userIN.password = md5_generator(password)
        userIN.save()

        return JsonResponse({"code": "0"} )
    else:
        return JsonResponse({"code": "1", "message": "잘못된 접근입니다."})


def agreement(request, num) :

    agree = UserAgree.objects.get(num=num)

    return render(request, 'user/agreement.html', {'agree': agree })


def ajax_findOldUser(request) :

    userName = request.GET.get("userName","")
    userPhone = request.GET.get("userPhone","")

    userInfo = UserInfo.objects.filter(name=userName, phone=userPhone, usertype="S-NORMAL")

    return render(request, 'user/ajax_findOldUser.html', {'userInfo': userInfo })


def comfirmPhone(requset):

    return "/"



def sendSMS( receiver, title, msg ) :

    send_url = 'https://apis.aligo.in/send/'  # 요청을 던지는 URL, 현재는 문자보내기

    # ================================================================== 문자 보낼 때 필수 key값
    # API key, userid, sender, receiver, msg
    # API키, 알리고 사이트 아이디, 발신번호, 수신번호, 문자내용

    sms_data = {'key': 'cl40fh7a45efop5rdoz2vhyqpizi5eus',  # api key
                'userid': 'ksnpick',  # 알리고 사이트 아이디
                'sender': '01028814491',  # 발신번호
                'receiver': receiver,  # 수신번호 (,활용하여 1000명까지 추가 가능)
                'msg': msg,  # 문자 내용
                'msg_type': title,  # 메세지 타입 (SMS, LMS)
                'title': 'title',  # 메세지 제목 (장문에 적용)
                'destination': receiver,  # %고객명% 치환용 입력
                # 'rdate' : '예약날짜',
                # 'rtime' : '예약시간',
                # 'testmode_yn' : '' #테스트모드 적용 여부 Y/N
                }
    send_response = requests.post(send_url, data=sms_data)

    return send_response.json()

