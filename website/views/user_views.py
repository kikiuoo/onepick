import requests
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.utils import timezone
import json

from picktalk.models import *

import hashlib
import random
from django.db import connection
from myonepick.common import *
from django.views.decorators.csrf import csrf_exempt

loginUrl = "https://myonepick.com/users/login"
#loginUrl = "http://localhost:8000/users/login"


def agreement(request, num) :
    nUrl = nowDevice(request)

    agree = UserAgree.objects.get(num=num)

    return render(request,  nUrl + '/user/agreement.html', {'agree': agree })


def userMypage(request, type) :
    nUrl = nowDevice(request)

    try:
        cursor = connection.cursor()
        user = request.session.get('id', '')

        userInfo = UserInfo.objects.get(userid=user)

        if userInfo.name == "" or userInfo.name == None or userInfo.phone == "" or userInfo.phone == None \
                or userInfo.email == "" or userInfo.email == None or userInfo.birth == "" or userInfo.birth == None:
            return redirect("/login/joinUser/")

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

    return render(request, nUrl + '/user/mypage.html', {"type" : type, "userInfo" : userInfo, "company" : company,
                                                "data1" : data1, "data2" : data2, "data3":data3 })

def updateUser(request) :
    nUrl = nowDevice(request)

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
    if userInfo.phone :
        phone[0] = userInfo.phone[0:3]
        phone[1] = userInfo.phone[3:7]
        phone[2] = userInfo.phone[7:11]
    else:
        phone = ["", "", ""]

    return render(request, nUrl + '/user/userInfo.html', {"userInfo" : userInfo, "userCompany" : userCompany,
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
    nUrl = nowDevice(request)

    userName = request.GET.get("userName","")
    userPhone = request.GET.get("userPhone","")

    userInfo = UserInfo.objects.filter(name=userName, phone=userPhone, usertype="S-NORMAL")

    return render(request, nUrl + '/user/ajax_findOldUser.html', {'userInfo': userInfo })


def ajax_findUser(request) :

    userName = request.GET.get("userName","")
    userPhone = request.GET.get("userPhone","")

    userInfo = UserInfo.objects.filter(name=userName, phone=userPhone)

    return render(request, nUrl + '/user/ajax_findOldUser.html', {'userInfo': userInfo })


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
    nUrl = nowDevice(request)

    return render(request, nUrl + '/user/userPW.html')

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


def quit(request) :

    nUrl = nowDevice(request)
    user = request.session.get('id', '')

    userInfo = UserInfo.objects.get(userid=user)

    return render(request, nUrl + '/user/quit.html', { "userInfo" : userInfo })


def quitCallback(request) :

    quitCause = request.POST.get('quitCause', '')
    quitEtcCause = request.POST.get("quitEtcCause", "")

    print(quitCause)

    if quitCause == "etc" :
        quit = quitEtcCause
    else :
        quit = quitCause

    nowTime = timezone.now()
    user = request.session.get('id', '')

    userInfo = UserInfo.objects.get(userid=user)
    profiles = ProfileInfo.objects.filter(userid=user)

    for profile in profiles:
        saveDelete = ProfileInfoDelete.objects.create(
            num=profile.num,
            userid=profile.userid,
            profileimage=profile.profileimage,
            detailimage=profile.detailimage,
            artimage=profile.artimage,
            height=profile.height,
            weight=profile.weight,
            topsize=profile.topsize,
            bottomsize=profile.bottomsize,
            shoessize=profile.shoessize,
            skincolor=profile.skincolor,
            haircolor=profile.haircolor,
            foreign=profile.foreign,
            mainyoutube=profile.mainyoutube,
            youtube=profile.youtube,
            talent=profile.talent,
            comment=profile.comment,
            intercate=profile.intercate,
            intersubcate=profile.intersubcate,
            iscareer=profile.iscareer,
            careeryear=profile.careeryear,
            careermonth=profile.careermonth,
            regdate=profile.regdate,
            update=profile.update,
            viewcount=profile.viewcount,
            cviewcount=profile.cviewcount,
            pickcount=profile.pickcount,
            public=profile.public,
            contenttype=profile.contenttype
        )

        profile.delete()

    userDelSave = UserInfoQuit.objects.create(
        num=userInfo.num,
        userid=userInfo.userid,
        password=userInfo.password,
        nickname=userInfo.nickname,
        name=userInfo.name,
        phone=userInfo.phone,
        email=userInfo.email,
        birth=userInfo.birth,
        birthtype=userInfo.birthtype,
        gender=userInfo.gender,
        nationality=userInfo.nationality,
        finalschool=userInfo.finalschool,
        school=userInfo.school,
        major=userInfo.major,
        entertain=userInfo.entertain,
        military=userInfo.military,
        zipcode=userInfo.zipcode,
        addr1=userInfo.addr1,
        addr2=userInfo.addr2,
        instargram=userInfo.instargram,
        youtube=userInfo.youtube,
        agreeusage=userInfo.agreeusage,
        agreeprivacy=userInfo.agreeprivacy,
        agreeemail=userInfo.agreeemail,
        agreemarketing=userInfo.agreemarketing,
        agreesms=userInfo.agreesms,
        jointype=userInfo.jointype,
        regtime=userInfo.regtime,
        lastlogin=userInfo.lastlogin,
        logincount=userInfo.logincount,
        usertype=userInfo.usertype,
        quitreason=quit,
        quitdate=nowTime
    )

    userInfo.delete()

    del request.session['id']
    del request.session['userType']

    return redirect("/")

