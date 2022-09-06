import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template import  loader
from django.db import connection

import requests
from bs4 import BeautifulSoup

from picktalk.models import *
from django.db.models import Q
from django.utils import timezone

from myonepick.common import *


def mailMain(request):

    try:
        cursor = connection.cursor()

        query = "SELECT DISTINCT(email), num, NAME,  gender, birth, userType  " \
                "FROM user_info " \
                "WHERE ( agreeEmail = '1' or agreeEmail = 'Y' ) and email is not null and email != '' " \
                "order by name "

        result = cursor.execute(query)
        userList = cursor.fetchall()

        connection.commit()
        connection.close()

    except:
        connection.rollback()

    return render( request, "onepickAdmin/cs/mailing.html", {'pageType': "cs", "userList":userList })


def ajaxUserList(request):

    userType = request.GET['userType']
    geneder = request.GET['geneder']
    age1 = request.GET['age1']
    age2 = request.GET['age2']
    name = request.GET['name']

    where = ""

    if userType != "" :
        if userType == "NORMAL" :
            where = where + " and ( userType='" + userType + "' or userType='S-" + userType + "' )"
        elif userType == "COMPANY" :
            where = where + " and ( userType='" + userType + "' or userType='S-" + userType + "' )"
        else :
            where = where + " and userType='" + userType + "'"

    if geneder != "":
        where = where + " and gender='" + geneder + "'"

    if age1 != "" and age2 != "":
        nowTime = str(timezone.now())
        year = nowTime.split('-')

        age_1 = int(year[0]) - int(age1) + 1
        age_2 = int(year[0]) - int(age2) + 1

        where = where + " and birth >= '" + str(age_1) + "-01-01' and birth <= '" + str(age_2) + "-12-31' "

    if name != "":
        where = where + " and name='" + name + "'"

    try:
        cursor = connection.cursor()

        query = "SELECT DISTINCT(email), num, NAME,  gender, birth, userType  " \
                "FROM user_info " \
                "WHERE ( agreeEmail = '1' or agreeEmail = 'Y' ) and email is not null and email != ''  " + where

        result = cursor.execute(query)
        userList = cursor.fetchall()

        connection.commit()
        connection.close()

    except:
        connection.rollback()

    return render(request, 'onepickAdmin/cs/ajax_mailing.html', {'userList': userList})


def summerImageUpload(request) :
    file = request.FILES.getlist("file", "")
    for image in file:
        sub = image.name.split('.')[-1]
        url = uploadFile(image, "photos/mailing/", sub)  # 파일 업로드
        logoImage = url

    return JsonResponse({"code": "0", "url" :  logoImage})

def sendMail(request) :
    title = request.POST['title']
    content = request.POST['content']
    sendList = request.POST['sendList']

    send = sendList.split(",")

    nowTime = timezone.now()
    saveMail = MailList.objects.create(title=title, content=content, send=len(send), success=0, fail=0, regdate=nowTime)

    for sends in send :
        userInfo = UserInfo.objects.get(num=sends)

        mail = sendMails(title, content, userInfo.email)

        if mail == "OK" :
            saveMail.success = saveMail.success + 1
        else :
            saveMail.fail = saveMail.fail + 1

        mailDetail = MailDetail.objects.create(mailnum=saveMail.num, userid=userInfo.userid, status=mail, regdate=nowTime)
        saveMail.save()

    return JsonResponse({"code": "0"})

def mailList(request, page):

    block = 10
    start = (page - 1) * block

    mailAll = MailList.objects.all()

    try:
        cursor = connection.cursor()

        query = "SELECT *  FROM mail_list  order by num desc limit " + str(start) + ", " + str(block)

        result = cursor.execute(query)
        mailList = cursor.fetchall()

        connection.commit()
        connection.close()

    except:
        connection.rollback()

    allPage = int(len(mailAll) / block) + 1

    paging = getPageList_v2(page, allPage)

    return render( request, "onepickAdmin/cs/mailList.html",
                   {'pageType': "cs", "mailList":mailList, "paging":paging, "page" : page,
                    "leftPage" : page-1, "rightPage" : page+1, "lastPage" : allPage })

def mailDetail(request, num):

    mailList = MailList.objects.get(num=num)

    try:
        cursor = connection.cursor()

        query = "SELECT `name`, userType, email, `status`, regDate " \
                "FROM mail_detail AS md LEFT JOIN user_info AS ui " \
                "     ON md.userID = ui.userID " \
                "WHERE mailNum = '"+str(num)+"' "

        result = cursor.execute(query)
        sendList = cursor.fetchall()

        connection.commit()
        connection.close()

    except:
        connection.rollback()

    return render( request, "onepickAdmin/cs/mailDetail.html"
                   , {'pageType': "cs", "mailList":mailList, "sendList" : sendList })


def youtube(request):

    userError = UserError.objects.all()

    return render( request, "onepickAdmin/cs/youtube.html", {'pageType': "cs", "userError" : userError })

def youtubeLink(request):
    link = request.GET.get('link',"")

    return render( request, "onepickAdmin/cs/youtubeLink.html", { "link" : link })

def checkYoutube(request) :
    # UserError 테이블 비우기
    # UserError.objects.all().delete()

    cursor = connection.cursor()

    query = "SELECT ui.userID, NAME, email, gender, pr.youtube, birth, userType  " \
            "FROM profile_info AS pr LEFT JOIN user_info AS ui " \
            "     ON pr.userID = ui.userID  " \
            "WHERE lastLogin >= '2022-01-01' " \
            "GROUP BY userID ORDER BY ui.userID limit 10"

    result = cursor.execute(query)
    loginList = cursor.fetchall()

    for user in loginList:

        if user[4] == "" or user[4] == None:
            # checkUserInfo(user)
            print("aa")
        else:
            youtubes = user[4].split('|')

            for youtu in youtubes:

                print(youtu)

                page = requests.get("http://localhost:8080/onepickAdmin/cs/youtubeLink/?link=" + str(youtu))
                soup = BeautifulSoup(page.text, "html.parser")

                elements = soup.select('div.ytp-title-link')

                print(elements)

                for index, element in enumerate(elements, 1):
                    print("{} 번째 게시글의 제목: {}".format(index, element.text))

    return ""

def checkUserInfo(user) :

    userFind = UserError.objects.filter(email=user[2])

    if len(userFind) == 0 :
        UserError.objects.create(email=user[2],name=user[1],gender=user[3],usertype=user[7],brith=user[6])

    return ""