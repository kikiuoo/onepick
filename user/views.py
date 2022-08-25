import requests
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.utils import timezone
import json
import os

from picktalk.models import *

import hashlib
import random
from django.conf import settings
from django.db import connection
from myonepick.common import *
from django.views.decorators.csrf import csrf_exempt

loginUrl = "https://myonepick.com/users/login"
#loginUrl = "http://localhost:8000/users/login"


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

    returnUrl = userLogin(request, "kakao_"+id, email, "", "", "", "KAKAO")

    return redirect(returnUrl)




# 구글 로그인 API 호출
def googleLogin(request):
    app_key = "329992018312-vcfcr44dgjat5q47pf91902rp8hh1ei0.apps.googleusercontent.com"
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
    client_id = "329992018312-vcfcr44dgjat5q47pf91902rp8hh1ei0.apps.googleusercontent.com"
    client_secret = "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"
    #AIzaSyDK6_FmteverNdo8r3womycHKb8MbboFbo

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
    print(sub + " " + email)

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
    #email = response.get("email", None)
    #gender = response.get("gender", None)
    #name = response.get("name", None)
    #birthday = response.get("birthday", None)
    #birthyear = response.get("birthyear", None)

    returnUrl = userLogin(request, "naver_"+id, "", "", "", "", "NAVER")

    return redirect(returnUrl)


def localLogin (request) :
    reUrl = request.GET.get('reUrl',"")

    return render(request, 'user/login.html', {"reUrl":reUrl})

def localLoginCallback (request) :
    username = request.GET['username']
    password = request.GET['password']

    pw = md5_generator(password)
    userIN = UserInfo.objects.filter(userid=username, password=pw)

    if userIN.count() > 0:
        userIN = UserInfo.objects.get(userid=username, password=pw)

        request.session['id'] = userIN.userid
        request.session['userType'] = userIN.usertype

        #request.session['id'] = 'ahdongkim1004'
        #request.session['userType'] = 'NORMAL'

        request.session.set_expiry(0)

        updateLastVisit(userIN.userid)

        return JsonResponse({"code": "0"})
    else:
        return JsonResponse({"code": "1", 'message': "아이디 혹은 비밀번호가 일치 하지 않습니다."})


def userLogin(request, id, email, gender, name, birth, joinType) :

    returnUrl = ""
    isUser = UserInfo.objects.filter(userid=id)

    if isUser.count() <= 0 :
        nowTime = timezone.now()
        addUser = UserInfo.objects.create(userid=id, email=email, jointype=joinType, gender=gender, name=name,
                                          birth=birth, regtime=nowTime, lastlogin=nowTime, logincount=1,
                                          usertype="NORMAL")
        key = addUser.userid

        returnUrl = "/users/join/" + str(key) + "/social/"
    else :
        isUser = UserInfo.objects.get(userid=id)

        userID = isUser.userid
        userType = isUser.usertype

        request.session['id'] = userID
        request.session['userType'] = userType
        request.session.set_expiry(0)

        if isUser.phone == None or isUser.email == None or isUser.name == None or isUser.usertype == "S-NORMAL" \
            or isUser.phone == "" or isUser.email == "" or isUser.name == "" :
            returnUrl = "/users/join/" + str(userID) + "/social/"
        else :
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


@csrf_exempt
def joinUpdate(request):

    num = request.POST['num']
    joinType = request.POST['joinType']
    userType = request.POST.get('userType',"")
    userID = request.POST.get('user_id',"")
    oldUserID = request.POST.get('oldUserID',"")
    pw1 = request.POST.get('pw1',"")
    name = request.POST['name']
    email1 = request.POST['email1']
    email2 = request.POST['email2']
    phone1 = request.POST['phone1']
    phone2 = request.POST['phone2']
    phone3 = request.POST['phone3']
    brith1 = request.POST.get('brith1',"")
    brith2 = request.POST.get('brith2',"")
    brith3 = request.POST.get('brith3',"")
    gender = request.POST.get('gender',"")
    addr1 = request.POST.get('addr1',"")
    addr2 = request.POST.get('addr2',"")
    companyName = request.POST.get('companyName',"")
    license = request.POST.get('license',"")
    companyAddr1 = request.POST.get('companyAddr1',"")
    companyAddr2 = request.POST.get('companyAddr2',"")
    webSite = request.POST.get('webSite',"")
    logo = request.FILES.getlist('logo[]')
    licenseImage = request.FILES.getlist('licenseImage[]')
    artLicense = request.FILES.getlist('artLicense[]')

    phoneCheck = request.POST.get('phoneCheck',"")
    emailCheck = request.POST.get('emailCheck',"")

    if phoneCheck != "1" :
        phoneCheck = "0"

    if emailCheck != "1":
        emailCheck = "0"

    print ( oldUserID )

    if oldUserID == "" :
        userInfo = UserInfo.objects.get(num=num)
    else :
        userInfo = UserInfo.objects.get(userid=oldUserID)
        updateUserID(userID, oldUserID)

    if joinType == "oldUser" :
        userInfo.password = md5_generator(pw1)
        userInfo.jointype = "OLDUSER"

    userInfo.name = name
    userInfo.email = email1+"@"+email2
    userInfo.phone = phone1+phone2+phone3
    userInfo.gender = gender
    userInfo.birth = brith1+"-"+brith2+"-"+brith3

    userInfo.agreeusage = "1"
    userInfo.agreeprivacy = "1"
    userInfo.agreemarketing = "1"
    userInfo.agreeemail = emailCheck
    userInfo.agreesms = phoneCheck

    if userType == "NORMAL" or  userType == "S-NORMAL" :
        # 일반회원 등록
        userInfo.addr1 = addr1
        userInfo.addr2 = addr2
        userInfo.usertype = "NORMAL"
    else :
        userInfo.usertype = "S-COMPANY"

        nowTime = timezone.now()

        count = 0
        # 로고
        for image in logo:
            count = count + 1
            sub = image.name.split('.')[-1]
            url = uploadFile(image, "photos/company/", sub)
            logoImage = url

        count = 0
        for image in licenseImage:
            count = count + 1
            sub = image.name.split('.')[-1]
            url = uploadFile(image, "photos/company/", sub)
            licenseImages = url

        count = 0
        for image in artLicense:
            count = count + 1
            sub = image.name.split('.')[-1]
            url = uploadFile(image, "photos/company/", sub)
            artLicenses = url


        userCompany = UserCompany.objects.create(userid=userID, logoimage=logoImage, licenseimage=licenseImages, artlicenseimage=artLicenses,
                                                 license=license,companyname=companyName, addr1=companyAddr1, addr2=companyAddr2, website=webSite,
                                                 regtime=nowTime)

    userInfo.save()

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
        userID = request.GET['userID']
        password = request.GET['password']

        userIN = UserInfo.objects.get(userid=userID)
        userIN.password = md5_generator(password)
        userIN.save()

        return JsonResponse({"code": "0"} )
    else:
        return JsonResponse({"code": "1", "message": "잘못된 접근입니다."})


def agreement(request, num) :

    agree = UserAgree.objects.get(num=num)

    return render(request, 'user/agreement.html', {'agree': agree })


def userMypage(request, type) :

    try:
        cursor = connection.cursor()
        user = request.session.get('id', '')

        userInfo = UserInfo.objects.get(userid=user)

        if type == "user" :
            company = ""
            data1 = ProfileInfo.objects.filter(userid=user, isdelete=0)
            query = "SELECT  ai.num, ai.title, ps.comment, UC.logoImage " \
                    "FROM profile_suggest AS ps LEFT JOIN audition_info AS ai ON ps.auditionNum = ai.num " \
                    "     LEFT JOIN user_company AS UC ON ai.userID  = UC.userID " \
                    "WHERE ps.userID = '"+user+"' and ai.isDelete = '0'"

            result = cursor.execute(query)
            data2 = cursor.fetchall()

            query = "SELECT  ai.num, ai.title, ai.endDate, ai.ordinary, UC.logoImage " \
                    "FROM audition_pick AS ap LEFT JOIN audition_info AS ai ON ap.auditionNum = ai.num " \
                    "     LEFT JOIN user_company AS UC ON ai.userID  = UC.userID " \
                    "WHERE ap.userID = '"+user+"' and ai.isDelete = '0'"

            result = cursor.execute(query)
            data3 = cursor.fetchall()

        else :
            company = UserCompany.objects.get(userid=user)

            data1 = AuditionInfo.objects.filter(userid=user, isdelete="0").order_by("-regtime")
            query = "SELECT p.num, profileImage, height, weight, ui.name, ui.birth, ui.entertain, ui.gender, ui.military, ui.school, ui.major, talent, ps.COMMENT " \
                    "FROM profile_suggest AS ps LEFT JOIN profile_info AS p ON ps.profileNum = p.num " \
                    "     LEFT JOIN user_info AS ui ON ps.userID  = ui.userID  " \
                    "WHERE ps.suUserID = '"+user+"' and p.isDelete = '0' " \
                    "order by ps.regTime desc limit 2"

            result = cursor.execute(query)
            data2 = cursor.fetchall()

            query = "SELECT  p.num, profileImage, height, weight, viewCount, pickCount, cViewCount, ui.name, ui.birth, ui.entertain, ui.gender, ui.military, ui.school, ui.major, talent, COMMENT, mainYoutube, isCareer " \
                    "FROM profile_pick AS pp LEFT JOIN profile_info AS p ON pp.profileNum = p.num " \
                    "     LEFT JOIN user_info AS ui ON p.userID  = ui.userID  " \
                    "WHERE pp.userID = '"+user+"'  and p.isDelete = '0' " \
                    "order by pp.regTime desc  limit 2"

            result = cursor.execute(query)
            data3 = cursor.fetchall()

        connection.commit()
        connection.close()

    except:
        connection.rollback()

    return render(request, 'user/mypage.html', {"type" : type, "userInfo" : userInfo, "company" : company,
                                                "data1" : data1, "data2" : data2, "data3":data3 })

def updateUser(request) :

    user = request.session.get('id', '')

    userInfo = UserInfo.objects.get(userid=user)

    if userInfo.email :
        email = userInfo.email.split('@')
    else :
        email = ["", ""]

    birth = ""
    userCompany = ""
    if userInfo.usertype == "NORMAL" or  userInfo.usertype == "S-NORMAL" :
        birth = userInfo.birth.split('-')

    else :
        userCompany = UserCompany.objects.get(userid=user)

    phone = ["","",""]
    phone[0] = userInfo.phone[0:3]
    phone[1] = userInfo.phone[3:7]
    phone[2] = userInfo.phone[7:11]

    return render(request, 'user/userInfo.html', {"userInfo" : userInfo, "userCompany" : userCompany,
                                                  "email" : email, "birth":birth, "phone" : phone} )


def updateCallback(request) :

    userID = request.POST.get("user_id", "")
    userInfo = UserInfo.objects.get(userid=userID)

    password = request.POST.get("pw1", "")
    name = request.POST.get("name", "")
    email1 = request.POST.get("email1", "")
    email2 = request.POST.get("email2", "")
    phone1 = request.POST.get("phone1", "")
    phone2 = request.POST.get("phone2", "")
    phone3 = request.POST.get("phone3", "")

    phoneCheck = request.POST.get('phoneCheck',"")
    emailCheck = request.POST.get('emailCheck',"")

    print( "adfajdflkajsdfl ajd" + phoneCheck + "  sdfsdfsdfsdf " + emailCheck)

    if phoneCheck != "1" :
        phoneCheck = "0"

    if emailCheck != "1":
        emailCheck = "0"

    userInfo.agreeemail = emailCheck
    userInfo.agreesms = phoneCheck

    if userInfo.usertype == "NORMAL" or userInfo.usertype == "S-NORMAL" : # 일반 회원

        brith1 = request.POST.get("brith1", "")
        brith2 = request.POST.get("brith2", "")
        brith3 = request.POST.get("brith3", "")
        gender = request.POST.get("gender", "")
        addr1 = request.POST.get("addr1", "")
        addr2 = request.POST.get("addr2", "")

        if password != "":
            userInfo.password = md5_generator(password)

        userInfo.name = name
        userInfo.email = email1 + "@" + email2
        userInfo.phone = phone1 + phone2 + phone3
        userInfo.birth = brith1 + "-" + brith2 + "-" +brith3
        userInfo.gender = gender
        userInfo.addr1 = addr1
        userInfo.addr2 = addr2
        userInfo.usertype = "NORMAL"

        url = "/users/mypage/user/"

    else :

        if password != "":
            userInfo.password = md5_generator(password)

        userCompany = UserCompany.objects.get(userid=userID)

        companyName = request.POST.get("companyName", "")
        license = request.POST.get("license", "")
        companyAddr1 = request.POST.get("companyAddr1", "")
        companyAddr2 = request.POST.get("companyAddr2", "")
        webSite = request.POST.get("webSite", "")

        logoImg = request.POST.get("logoImg", "")
        licenseImg = request.POST.get("licenseImg", "")
        artLicenseImg = request.POST.get("artLicenseImg", "")

        logo = request.FILES.getlist("logo[]", "")
        licenseImage = request.FILES.getlist("licenseImage[]", "")
        artLicense = request.FILES.getlist("artLicense[]", "")

        nowTime = timezone.now()
        count = 0;
        # 로고
        logoImage = logoImg
        if len(logo) > 0:
            # 기존 이미지 삭제
            for rmImages in logoImg:
                if (rmImages == ""): continue
                deleteFile(rmImages)

            for image in logo:
                sub = image.name.split('.')[-1]
                url = uploadFile(image, "photos/company/", sub)  # 파일 업로드
                logoImage = url
                count = count + 1

        licenseImages = licenseImg
        if len(licenseImage) > 0:
            # 기존 이미지 삭제
            for rmImages in licenseImg:
                if (rmImages == ""): continue
                deleteFile(rmImages)

            for image in licenseImage:
                sub = image.name.split('.')[-1]
                url = uploadFile(image, "photos/company/", sub)  # 파일 업로드
                licenseImages = url
                count = count + 1

        artLicenses = artLicenseImg
        if len(artLicense) > 0:
            # 기존 이미지 삭제
            for rmImages in artLicenseImg:
                if (rmImages == ""): continue
                deleteFile(rmImages)

            for image in artLicense:
                sub = image.name.split('.')[-1]
                url = uploadFile(image, "photos/company/", sub)  # 파일 업로드
                artLicenses = url
                count = count + 1

        userInfo.name = name
        userInfo.email = email1 + "@" + email2
        userInfo.phone = phone1 + phone2 + phone3

        userCompany.name = companyName
        userCompany.license = license
        userCompany.logoimage = logoImage
        userCompany.licenseimage = licenseImages
        userCompany.artlicenseimage = artLicenses
        userCompany.addr1 = companyAddr1
        userCompany.addr2 = companyAddr2
        userCompany.website = webSite

        userCompany.save()

        url = "/users/mypage/company/"

    userInfo.save()

    return redirect(url)

def ajax_findOldUser(request) :

    userName = request.GET.get("userName","")
    userPhone = request.GET.get("userPhone","")

    userInfo = UserInfo.objects.filter(name=userName, phone=userPhone, usertype="S-NORMAL")

    return render(request, 'user/ajax_findOldUser.html', {'userInfo': userInfo })


def ajax_findUser(request) :

    userName = request.GET.get("userName","")
    userPhone = request.GET.get("userPhone","")

    userInfo = UserInfo.objects.filter(name=userName, phone=userPhone)

    return render(request, 'user/ajax_findOldUser.html', {'userInfo': userInfo })


def ajax_phoneComfirm(request) :

    userPhone = request.GET.get("phoneNum","")
    certifier = ""

    isUser = UserInfo.objects.filter(phone=userPhone, usertype="NORMAL") | UserInfo.objects.filter(phone=userPhone, usertype="COMPANY")  | UserInfo.objects.filter(phone=userPhone, usertype="S-COMPANY")

    if isUser.count() > 0 :
        return JsonResponse({"code": "1", "message" :  "이미 등록된 전화번호입니다."})
    else :
        while len(certifier) < 4:
            num = random.randint(0, 9)
            certifier = certifier + str(num)

        nowTime = timezone.now()
        saveSms = UserSms.objects.create(phonenum=userPhone, certifier=certifier, regdate=nowTime)

        send = sendSMS(userPhone, "인증번호 전송", "[ONEPICK 본인확인] 인증번호 [" + certifier + "]를 입력해주세요.")

        return JsonResponse({"code": "0"})

def ajax_pwPhoneComfirm(request) :

    userID = request.GET.get("userID","")
    userPhone = request.GET.get("phoneNum","")
    certifier = ""

    isUser = UserInfo.objects.filter(userid=userID, phone=userPhone)

    if isUser.count() > 0 :
        while len(certifier) < 4:
            num = random.randint(0, 9)
            certifier = certifier + str(num)

        nowTime = timezone.now()
        saveSms = UserSms.objects.create(phonenum=userPhone, certifier=certifier, regdate=nowTime)

        send = sendSMS(userPhone, "인증번호 전송", "[ONEPICK 본인확인] 인증번호 [" + certifier + "]를 입력해주세요.")

        return JsonResponse({"code": "0"})
    else :
        return JsonResponse({"code": "1", "message" :  "아이디, 전화번호를 확인해주세요."})


def ajax_checkConfirm(request) :

    userPhone = request.GET.get("phoneNum","")
    confirm = request.GET.get("confirm","")

    findSMS = UserSms.objects.filter(phonenum=userPhone).order_by("-num")[:1]

    for row in findSMS :
        saveConfirm = row.certifier

    code = ""
    msg = ""
    if confirm == saveConfirm :
        findSMS = UserSms.objects.filter(phonenum=userPhone).order_by("-num")
        findSMS.delete()
        code = "0"
    else :
        code = "1"
        msg = "입력한 인증번호가 다릅니다."

    return JsonResponse({"code": code, "message" :  msg})

def comfirmPhone(requset):

    return "/"





def updateUserID(userID, oldUserID) :

    userdel = UserInfo.objects.filter(userid=userID)
    userdel.delete()
    userInfo = UserInfo.objects.filter(userid=oldUserID)
    for row in userInfo :
        row.userid = userID
        row.save()

    userCompany = UserCompany.objects.filter(userid=oldUserID).update(userid=userID)
    audiInfo = AuditionInfo.objects.filter(userid=oldUserID).update(userid=userID)
    audiPick = AuditionPick.objects.filter(userid=oldUserID).update(userid=userID)

    proCareer = ProfileCareer.objects.filter(userid=oldUserID).update(userid=userID)
    proComment = ProfileComment.objects.filter(userid=oldUserID).update(userid=userID)
    proEtcCar = ProfileEtccareer.objects.filter(userid=oldUserID).update(userid=userID)
    proInfo = ProfileInfo.objects.filter(userid=oldUserID).update(userid=userID)
    proPick = ProfilePick.objects.filter(userid=oldUserID).update(userid=userID)

    qaQandA = QaQanda.objects.filter(userid=oldUserID).update(userid=userID)
    qaComment = QaQandaComment.objects.filter(userid=oldUserID).update(userid=userID)

    return ""


def updatePW(request) :

    return render(request, 'user/userPW.html')

def updatePWCallback(request) :

    user = request.session.get('id', '')
    nowPW = request.GET.get("nowPW", "")
    pw1 = request.GET.get("pw1", "")

    findPassword = md5_generator(nowPW)
    userInfo = UserInfo.objects.filter(userid=user, password=findPassword)

    if userInfo.count() == 0 :
        return JsonResponse({"code": "1", "message": "일치하는 정보가 없습니다."})
    else :
        userInfo = UserInfo.objects.get(userid=user)
        savePW = md5_generator(pw1)
        userInfo.password = savePW
        userInfo.save()

    return JsonResponse({"code": "0"})
