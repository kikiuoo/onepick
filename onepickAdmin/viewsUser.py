import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template import  loader
from django.db import connection

from picktalk.models import *
from django.db.models import Q
from django.utils import timezone
import xlwt

from myonepick.common import *

urlBase = "onepickAdmin/user/"

def list(request, type, page):
    user = request.session.get('adminID', '')
    if user == "" or user == None:
        message = '로그인 후 이용가능합니다..'
        return HttpResponse("<script>alert('" + message + "'); window.location.href = '/onepickAdmin'; </script>")

    block = 10
    start = (page - 1) * block
    end = page * block

    if type == "normal" :
        userList = UserInfo.objects.filter(usertype__contains="NORMAL", phone__isnull=False).order_by("-regtime")
    elif type == "company" :
        userList = UserInfo.objects.filter(usertype__contains="COMPANY", phone__isnull=False).order_by("-regtime")

    user = userList[start:end]
    allPage = int(len(userList) / block) + 1
    paging = getPageList_v2(page, allPage)

    return render( request, urlBase + "list.html", {'pageType': "user", "userList":user, "paging":paging, "page" : page,
                                                    "leftPage" : page-1, "rightPage" : page+1, "lastPage" : allPage, "type":type })


def listSearch(request, type, word, page):
    user = request.session.get('adminID', '')
    if user == "" or user == None:
        message = '로그인 후 이용가능합니다..'
        return HttpResponse("<script>alert('" + message + "'); window.location.href = '/onepickAdmin'; </script>")

    block = 10
    start = (page - 1) * block
    end = page * block

    try:
        cursor = connection.cursor()

        query = "SELECT *  FROM user_info " \
                "where ( `userID` like '%"+word+"%' or `name` like '%"+word+"%' or phone like '%"+word+"%' or `email` like '%"+word+"%' )"

        result = cursor.execute(query)
        userAll = cursor.fetchall()

        query = "SELECT *  " \
                "FROM user_info " \
                "where ( `userID` like '%"+word+"%' or `name` like '%"+word+"%' or phone like '%"+word+"%' or `email` like '%"+word+"%' )" \
                "order by num desc limit " + str(start) + ", " + str(block)

        result = cursor.execute(query)
        user = cursor.fetchall()

        connection.commit()
        connection.close()

    except:
        connection.rollback()

    allPage = int(len(userAll) / block) + 1
    paging = getPageList_v2(page, allPage)

    return render( request, urlBase + "listSearch.html",
                   {'pageType': "user", "userList":user, "paging":paging, "page" : page,
                    "leftPage" : page-1, "rightPage" : page+1, "lastPage" : allPage, "type":type, "word" : word })

def edit(request, num) :
    user = request.session.get('adminID', '')
    if user == "" or user == None:
        message = '로그인 후 이용가능합니다..'
        return HttpResponse("<script>alert('" + message + "'); window.location.href = '/onepickAdmin'; </script>")

    userInfo = UserInfo.objects.get(num=num)

    if userInfo.usertype == "COMPANY" or userInfo.usertype == "S-COMPANY" :
        company = UserCompany.objects.get(userid=userInfo.userid)
    else :
        company = ""

    if userInfo.email :
        email = userInfo.email.split('@')
    else :
        email = ["", ""]

    birth = ""
    if userInfo.usertype == "NORMAL" or  userInfo.usertype == "S-NORMAL" :
        birth = userInfo.birth.split('-')

    phone = ["","",""]
    if userInfo.phone:
        phone[0] = userInfo.phone[0:3]
        phone[1] = userInfo.phone[3:7]
        phone[2] = userInfo.phone[7:11]

    return render(request, urlBase + "edit.html",
                  {'pageType': "user", "userInfo" :  userInfo, "company" :company,
                   'email':email, "birth":birth, "phone":phone})

def editCallback(request) :

    userID = request.POST.get("user_id", "")
    userInfo = UserInfo.objects.get(userid=userID)

    name = request.POST.get("name", "")
    email1 = request.POST.get("email1", "")
    email2 = request.POST.get("email2", "")
    phone1 = request.POST.get("phone1", "")
    phone2 = request.POST.get("phone2", "")
    phone3 = request.POST.get("phone3", "")

    if userInfo.usertype == "NORMAL" or userInfo.usertype == "S-NORMAL" : # 일반 회원

        brith1 = request.POST.get("brith1", "")
        brith2 = request.POST.get("brith2", "")
        brith3 = request.POST.get("brith3", "")
        gender = request.POST.get("gender", "")
        addr1 = request.POST.get("addr1", "")
        addr2 = request.POST.get("addr2", "")

        userInfo.name = name
        userInfo.email = email1 + "@" + email2
        userInfo.phone = phone1 + phone2 + phone3
        userInfo.birth = brith1 + "-" + brith2 + "-" +brith3
        userInfo.gender = gender
        userInfo.addr1 = addr1
        userInfo.addr2 = addr2
        userInfo.usertype = "NORMAL"

        url = "/onepickAdmin/user/list/normal/1/"

    else :

        userCompany = UserCompany.objects.get(userid=userID)

        companyName = request.POST.get("companyName", "")
        license = request.POST.get("license", "")
        companyAddr1 = request.POST.get("companyAddr1", "")
        companyAddr2 = request.POST.get("companyAddr2", "")
        webSite = request.POST.get("webSite", "")

        userInfo.name = name
        userInfo.email = email1 + "@" + email2
        userInfo.phone = phone1 + phone2 + phone3

        userCompany.name = companyName
        userCompany.license = license
        userCompany.addr1 = companyAddr1
        userCompany.addr2 = companyAddr2
        userCompany.website = webSite

        userCompany.save()

        url = "/onepickAdmin/user/list/company/1/"

    userInfo.save()


    nowTime = str(timezone.now())
    user = request.session.get('adminID', '')
    adminLog = AdminLog.objects.create(userid=user, viewtype="user_update", content=userInfo.num, regdate=nowTime)

    return redirect(url)


def updateComany (request) :
    num = request.GET.get("num", "")

    userInfo = UserInfo.objects.get(num=num)

    userInfo.usertype = "COMPANY"
    userInfo.save()

    nowTime = str(timezone.now())
    user = request.session.get('adminID', '')
    adminLog = AdminLog.objects.create(userid=user, viewtype="user_update", content=num, regdate=nowTime)

    return JsonResponse({"code": "0"} )

def addCompany(request):
    user = request.session.get('adminID', '')
    if user == "" or user == None:
        message = '로그인 후 이용가능합니다..'
        return HttpResponse("<script>alert('" + message + "'); window.location.href = '/onepickAdmin'; </script>")

    return render(request, urlBase + "addCompany.html", {'pageType': "notice"})


def excel(request, type, word):
    response = HttpResponse(content_type="application/vnd.ms-excel")
    response["Content-Disposition"] = 'attachment;filename*=UTF-8\'\'user_info.xls'
    wb = xlwt.Workbook(encoding='ansi')  # encoding은 ansi로 해준다.
    ws = wb.add_sheet('회원 정보')  # 시트 추가

    row_num = 0
    col_names = ['이름', '회원그룹', '연락처', '나이' ,'성별' ,'주소' , '가입일', '가입경로', '마지막 로그인 시간', '탈퇴유무', '프로필작성유무' ]

    # 열이름을 첫번째 행에 추가 시켜준다.
    for idx, col_name in enumerate(col_names):
        ws.write(row_num, idx, col_name)

    # 데이터 베이스에서 유저 정보를 불러온다.
    try:
        cursor = connection.cursor()

        if type == "normal":
            userType = "NORMAL"
        elif type == "company":
            userType = "COMPANY"

        if word == "|" :
            word = ""

        query = "SELECT name, userType, phone, birth ,gender, addr1, regTime, joinType, lastLogin, " \
                "       'N' as dropUser, (SELECT COUNT(*) FROM profile_info WHERE userID = A.userID) AS proCount   " \
                "FROM user_info as A " \
                "where userType like '%"+userType+"%' and ( `userID` like '%" + word + "%' or `name` like '%" + word + "%' or phone like '%" + word + "%' or `email` like '%" + word + "%' ) " \
                      " and phone != '' " \
                "order by num desc "

        result = cursor.execute(query)
        user = cursor.fetchall()

        connection.commit()
        connection.close()

    except:
        connection.rollback()

    # 유저정보를 한줄씩 작성한다.

    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'yyyy-mm-dd'

    for row in user:
        row_num += 1
        for col_num, attr in enumerate(row):
            if col_num == 1 :
                if attr == "S-COMPANY" :
                    ws.write(row_num, col_num, "미승인기업")
                elif attr == "COMPANY" :
                    ws.write(row_num, col_num, "기업회원")
                elif attr == "NORMAL" :
                    ws.write(row_num, col_num, "일반회원")
                elif attr == "S-NORMAL" :
                    ws.write(row_num, col_num, "미이전회원")

            elif col_num == 3 :

                birth = attr.split('-')
                nowTime = str(timezone.now())
                year = nowTime.split('-')

                if birth[0] != "":
                    age = int(year[0]) - int(birth[0]) + 1
                else:
                    age = "-"
                ws.write(row_num, col_num, age)

            elif col_num == 4 :
                if attr == "girl" :
                    ws.write(row_num, col_num, "여성")
                elif attr == "man" :
                    ws.write(row_num, col_num, "남성")

            elif col_num == 7 :
                if attr == "NAVER" :
                    ws.write(row_num, col_num, "네이버")
                elif attr == "KAKAO" :
                    ws.write(row_num, col_num, "카카오")
                elif attr == "GOOGLE" :
                    ws.write(row_num, col_num, "구글")
                elif attr == "FACEBOOK" :
                    ws.write(row_num, col_num, "페이스북")
                elif attr == "TWITTER" :
                    ws.write(row_num, col_num, "트위터")
                else :
                    ws.write(row_num, col_num, "기존회원")

            elif col_num == 6 or col_num == 8:
                ws.write(row_num, col_num, attr,date_format)

            elif col_num == 10:
                if int(attr) > 0 :
                    ws.write(row_num, col_num, "Y")
                else :
                    ws.write(row_num, col_num, "N")
            else :
                ws.write(row_num, col_num, attr)

    wb.save(response)

    nowTime = str(timezone.now())
    user = request.session.get('adminID', '')
    adminLog = AdminLog.objects.create(userid=user, viewtype="user_download", content=type, regdate=nowTime)

    return response


def logList(request, page):
    user = request.session.get('adminID', '')
    if user == "" or user == None:
        message = '로그인 후 이용가능합니다..'
        return HttpResponse("<script>alert('" + message + "'); window.location.href = '/onepickAdmin'; </script>")

    block = 10
    start = (page - 1) * block
    end = page * block

    logList = AdminLog.objects.all().order_by("-regdate")

    log = logList[start:end]
    allPage = int(len(logList) / block) + 1
    paging = getPageList_v2(page, allPage)

    return render( request, urlBase + "logList.html", {'pageType': "user", "logList":log, "paging":paging, "page" : page,
                                                    "leftPage" : page-1, "rightPage" : page+1, "lastPage" : allPage })
