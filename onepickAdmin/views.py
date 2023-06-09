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
    print("adminCheck 메소드 : onepickAdmin/views.py ")

    user = request.session.get('adminID', '')

    if user :
        returnURL = "onepickAdmin/main.html"

        noticeList = QaNotice.objects.all().order_by("-regdate")[:5]

        try:
            cursor = connection.cursor()
            query = "SELECT C, COUNT(*) AS counting " \
                    "FROM( " \
                    "	SELECT DATE_FORMAT(regTime,'%y/%m/%d') AS C " \
                    "	FROM user_info " \
                    "	WHERE  regTime >= '2021-12-01' " \
                    "	ORDER BY regTime " \
                    ")AS a " \
                    "GROUP BY C ORDER BY C DESC LIMIT 14 "

            result = cursor.execute(query)
            userDay = cursor.fetchall()

            userMax = getListMax(userDay)
            printUser = getBar(userDay, userMax)
            userLabel = getLabel(userMax)


            cursor = connection.cursor()
            query = "SELECT C , COUNT(*) AS counting " \
                    "FROM( " \
                    "	SELECT DATE_FORMAT(viewDay,'%y/%m/%d') AS C   " \
                    "	FROM view_count " \
                    ")AS a " \
                    "GROUP BY C  ORDER BY C DESC LIMIT 14"


            result = cursor.execute(query)
            connDay = cursor.fetchall()

            connMax = getListMax(connDay)
            printConn = getBar(connDay, connMax)
            connLabel = getLabel(connMax)


            cursor = connection.cursor()
            query = "SELECT C, COUNT(*) AS counting " \
                    "FROM( " \
                    "	SELECT DATE_FORMAT(accessTime,'%y/%m/%d') AS C " \
                    "	FROM user_login " \
                    "	WHERE accessTime >= '2021-01-01' " \
                    "	ORDER BY accessTime " \
                    ")AS a " \
                    "GROUP BY C ORDER BY C DESC LIMIT 14 "

            result = cursor.execute(query)
            loginDay = cursor.fetchall()

            loginMax = getListMax(loginDay)
            printLogin = getBar(loginDay, loginMax)
            loginLabel = getLabel(loginMax)

        except:
            connection.rollback()

        return render(request, returnURL, {'pageType': "home", "noticeList" : noticeList,
                                           "printUser" : printUser, "userLabel" : userLabel,
                                           "printConn" : printConn, "connLabel" : connLabel,
                                           "printLogin" : printLogin, "loginLabel" : loginLabel  })

    else :
        returnURL = "onepickAdmin/login/login.html"
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
        request.session['id'] = userIN.userid
        request.session['userType'] = userIN.usertype

        request.session.set_expiry(3600)

        return JsonResponse({"code": "0"})
    else:
        return JsonResponse({"code": "1", 'message': "아이디 혹은 비밀번호가 일치 하지 않습니다."})

def adminLogout (request) :
    del request.session['adminID']
    #del request.session['adminName']

    return JsonResponse({"code": "0"} )

def ajaxGetGraph(request) :
    print("ajaxGetGraph 메소드 : onepickAdmin/views.py ")

    dataType = request.GET['dataType']
    type = request.GET['type']
    print("dataType : ",dataType)
    print("type : ",type)

    try:
        cursor = connection.cursor()

        # 회원가입 수
        if dataType == "user" :
            if type == "day" :

                print ("일별누름")

                query = "SELECT C, COUNT(*) AS counting " \
                        "FROM( " \
                        "	SELECT DATE_FORMAT(regTime,'%y/%m/%d') AS C " \
                        "	FROM user_info " \
                        "	WHERE regTime >= '2022-12-01' " \
                        "	ORDER BY regTime " \
                        ")AS a " \
                        "GROUP BY C ORDER BY C DESC LIMIT 14 "
            elif type == "week" :
                query = "SELECT W, COUNT(*) AS counting  " \
                        "FROM( " \
                        "	SELECT DATE_FORMAT(regTime,'%U') AS W,DATE_FORMAT(regTime,'%Y') AS Y  " \
                        "	FROM user_info " \
                        "   where phone != ''" \
                        "	ORDER BY regTime " \
                        ")AS a " \
                        "GROUP BY Y, W ORDER BY Y DESC, W DESC LIMIT 14  "
            elif type == "month" :
                query = "SELECT C, COUNT(*) AS counting " \
                        "FROM( " \
                        "	SELECT DATE_FORMAT(regTime,'%Y/%m') AS C  " \
                        "	FROM user_info " \
                        "   where phone != ''" \
                        "	ORDER BY regTime " \
                        ")AS a " \
                        "GROUP BY C ORDER BY C DESC LIMIT 14 "

        # 접속자 수
        elif dataType == "connect":
            if type == "day":
                query = "SELECT C , COUNT(*) AS counting " \
                        "FROM( " \
                        "	SELECT DATE_FORMAT(viewDay,'%y/%m/%d') AS C   " \
                        "	FROM view_count " \
                        ")AS a " \
                        "GROUP BY C  ORDER BY C DESC LIMIT 14"

            elif type == "week":
                query = "SELECT W, COUNT(*) AS counting  " \
                        "FROM( " \
                        "	SELECT DATE_FORMAT(viewDay,'%U') AS W ,DATE_FORMAT(viewDay,'%Y') AS Y   " \
                        "	FROM view_count " \
                        ")AS a " \
                        "GROUP BY Y, W ORDER BY Y DESC, W DESC LIMIT 14  "
            elif type == "month":
                query = "SELECT C, COUNT(*) AS counting " \
                        "FROM( " \
                        "	SELECT DATE_FORMAT(viewDay,'%Y/%m') AS C  " \
                        "	FROM view_count " \
                        ")AS a " \
                        "GROUP BY C ORDER BY C DESC LIMIT 14 "

        elif dataType == "login":
            if type == "day":
                query = "SELECT C, COUNT(*) AS counting " \
                        "FROM( " \
                        "	SELECT DATE_FORMAT(accessTime,'%y/%m/%d') AS C " \
                        "	FROM user_login " \
                        "	WHERE accessTime >= '2022-12-01' " \
                        "	ORDER BY accessTime " \
                        ")AS a " \
                        "GROUP BY C ORDER BY C DESC LIMIT 14 "
            elif type == "week":
                query = "SELECT W, COUNT(*) AS counting  " \
                        "FROM( " \
                        "	SELECT DATE_FORMAT(accessTime,'%U') AS W,DATE_FORMAT(accessTime,'%Y') AS Y  " \
                        "	FROM user_login " \
                        "	ORDER BY accessTime " \
                        ")AS a " \
                        "GROUP BY Y, W ORDER BY Y DESC, W DESC LIMIT 14  "
            elif type == "month":
                query = "SELECT C, COUNT(*) AS counting " \
                        "FROM( " \
                        "	SELECT DATE_FORMAT(accessTime,'%Y/%m') AS C  " \
                        "	FROM user_login " \
                        "	ORDER BY accessTime " \
                        ")AS a " \
                        "GROUP BY C ORDER BY C DESC LIMIT 12 "

        result = cursor.execute(query)
        countList = cursor.fetchall()

        countMax = getListMax(countList)
        printList = getBar(countList, countMax)
        printLabel = getLabel(countMax)

    except:
        connection.rollback()

    return render(request, "onepickAdmin/ajax/getGraph.html", {"printList": printList, "printLabel": printLabel})

def getLabel(maxCount) :
    labelList = []
    labelSub = int(maxCount / 5)

    for num in range(0, 5):
        labelList.append(maxCount - (labelSub * num))

    return labelList

def getBar(barList, maxCount) :

    dateList = []
    countList = []
    for joinCount in barList:
        dateList.insert(0, joinCount[0])
        countList.insert(0, joinCount[1])

    persentList = []
    for joinCount in barList:
        persentList.insert(0, int(joinCount[1] / maxCount * 100))

    printList = [dateList, countList, persentList]

    return printList

def getListMax(barList) :
    userMax = 0
    for joinCount in barList:
        if userMax < joinCount[1]:
            userMax = joinCount[1]

    userMax = (int(int(userMax) / 10) + 1) * 10

    return userMax