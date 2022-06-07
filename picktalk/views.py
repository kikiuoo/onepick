import smtplib
from django.db.models import Subquery
from django.shortcuts import render
from django.http import HttpResponse
from django.template import  loader
from django.db import connection
from django.utils import timezone
from django.http import JsonResponse
from email.mime.text import MIMEText

from picktalk.models import *

# Create your views here.

# Index 페이지 Query 내용
def index(request):

    try :
        cursor = connection.cursor()

        # 메인 베너
        mainbanner = EventBanner.objects.filter(position="main")

        user = request.session.get('id', '')

        if user :
            query = "SELECT AI.num, AI.title, AI.endDate, AI.ordinary, UC.logoImage, (SELECT COUNT(*) FROM audition_pick WHERE userID = '" + user +"' AND auditionNum = AI.num ) AS audiPick " \
                    "FROM audition_info AS AI LEFT JOIN user_company AS UC ON AI.userID  = UC.userID " \
                    "where AI.isDelete = '0' or AI.isDelete is null " \
                    "order by AI.regTime desc LIMIT 8 "
        else :
            query = "SELECT AI.num, AI.title, AI.endDate, AI.ordinary, UC.logoImage, '0' AS audiPick " \
                    "FROM audition_info AS AI LEFT JOIN user_company AS UC ON AI.userID  = UC.userID " \
                    "where AI.isDelete = '0' or AI.isDelete is null " \
                    "order by AI.regTime desc LIMIT 8 "

        result = cursor.execute(query)
        auditions = cursor.fetchall()

        # 프로필
        if user:
            query = "SELECT p.num, profileImage, height, viewCount, pickCount, cViewCount, ui.name, ui.birth, ui.entertain, (SELECT COUNT(*) FROM profile_pick WHERE userID = '" + user +"' AND profileNum = p.num ) AS proPick " \
                    "FROM profile_info AS p LEFT JOIN user_info AS ui  ON p.userID = ui.userID " \
                    "WHERE public = '0' and isDelete = '0' " \
                    "ORDER BY regDate DESC " \
                    "LIMIT 4"
        else:
            query = "SELECT p.num, profileImage, height, viewCount, pickCount, cViewCount, ui.name, ui.birth, ui.entertain, '0' AS proPick " \
                    "FROM profile_info AS p LEFT JOIN user_info AS ui " \
                    "     ON p.userID = ui.userID " \
                    "WHERE public = '0' and isDelete = '0' " \
                    "ORDER BY regDate DESC  " \
                    "LIMIT 4"

        result = cursor.execute(query)
        profiles = cursor.fetchall()

        # 소베너 - 코드 변경 필요.
        subBanner = EventBanner.objects.filter(position="mainSub")

        connection.commit()
        connection.close()

    except :
        connection.rollback()

    return render(request, 'picktalk/index.html',
                  {'auditions': auditions, 'profiles': profiles , 'mainbanner' : mainbanner, 'subBanner' : subBanner })



def updatePick(request) :

    userID = request.GET["userID"]
    tableName = request.GET["tableName"]
    nowType = request.GET["nowType"]
    num = request.GET["num"]

    nowTime = timezone.now()

    if nowType == "off" : # off : 등록

        if tableName == "audition" :
            pick = AuditionPick.objects.create( auditionnum=num, userid=userID, regtime=nowTime )
        else :
            profiles = ProfileInfo.objects.get(num=num)
            profiles.pickcount = profiles.pickcount + 1
            profiles.save()
            pick = ProfilePick.objects.create( profilenum=num, userid=userID, regtime=nowTime )

    else : # on : 삭제

        if tableName == "audition" :
            pick = AuditionPick.objects.filter( auditionnum=num, userid=userID )
        else :
            profiles = ProfileInfo.objects.get(num=num)
            profiles.pickcount = profiles.pickcount - 1
            profiles.save()
            pick = ProfilePick.objects.filter( profilenum=num, userid=userID )

        pick.delete()

    return JsonResponse({"code": "0"})


def advertise(request) :

    return render(request, 'picktalk/advertise.html')



def advertise_callBack(request) :

    email = request.POST.get("email");
    title = request.POST.get("title");
    content = request.POST.get("content");

    saveAdvertise = QaAdvertise.objects.create(email=email, title=title, content=content)

    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login("ksonepick@gmail.com", "cfbfdpogjnchjrvk")

    msg = MIMEText(content + "\n\n담당자 메일:"+email)
    msg['Subject'] = title

    smtp.sendmail("ksonepick@gmail.com", "onepick@myonepick.com", msg.as_string())
    smtp.quit()


    return JsonResponse({"code": "0"})


def searchList(request, cateType, search, page) :
        cursor = connection.cursor()

        user = request.session.get('id', '')

        # 검색 결과 등록
        nowTime = timezone.now()
        nowTime = timezone.now()
        print(nowTime)
        saveSearch = UserSearch.objects.create(userid=user, search=search, regdate=nowTime)

        if cateType == "audition" :
            query = "SELECT ai.num, ai.title, cm.cateName, ai.career, ai.age, ai.endDate, ai.regTime, ai.ordinary, uc.companyName, DATEDIFF(NOW(),  ai.regTime) AS diffDate " \
                    "FROM audition_info AS ai LEFT JOIN cate_main AS cm ON ai.cate = cm.cateCode " \
                    "    LEFT JOIN  user_company AS uc ON ai.userID = uc.userID " \
                    "where (ai.isDelete = '0' or ai.isDelete is null ) and " \
                    "      ( title LIKE '%" + search + "%' OR age LIKE '%" + search + "%' OR gender LIKE '%" + search + "%' OR career LIKE '%" + search + "%' OR essential LIKE '%" + search + "%'  OR preparation LIKE '%" + search + "%' ) " \
                    "ORDER BY ai.regTime DESC limit 15"

        else :
            if user:
                query = "SELECT p.num , profileImage, height, weight, viewCount, pickCount, cViewCount, ui.name, ui.birth, ui.entertain, " \
                        "       ui.gender, ui.military, ui.school, ui.major, talent, comment, mainYoutube, isCareer, (SELECT COUNT(*) FROM profile_pick WHERE userID = '" + user + "' AND profileNum = p.num ) AS proPick " \
                        "FROM profile_info AS p LEFT JOIN user_info AS ui  ON p.userID = ui.userID " \
                        "     LEFT JOIN ( SELECT profileNum, COUNT(*) AS career FROM profile_career WHERE title LIKE '%" + search + "%' OR `role` LIKE '%" + search + "%' group by profileNum ) AS c ON p.num = c.profileNum " \
                        "     LEFT JOIN ( SELECT profileNum, COUNT(*) AS etcCareer FROM profile_etccareer WHERE title LIKE '%" + search + "%' OR `role` LIKE '%" + search + "%' group by profileNum ) AS d ON p.num = d.profileNum " \
                        "WHERE public = '0' and isDelete = '0' and  " \
                        "      ( career > 0 OR etcCareer > 0 OR `foreign` LIKE '%" + search + "%' OR talent LIKE '%" + search + "' OR `comment` LIKE '%" + search + "%' OR `careerYear` LIKE '%" + search + "%' OR `careerMonth` LIKE '%" + search + "%' " \
                        "        OR `foreign` LIKE '%" + search + "%' OR `birth` LIKE '%" + search + "%' OR `finalSchool` LIKE '%" + search + "%' OR `school` LIKE '%" + search + "%' OR `major` LIKE '%" + search + "%' OR `entertain` LIKE '%" + search + "%' OR `military` LIKE '%" + search + "%')  " \
                        "ORDER BY regDate DESC " \
                        "LIMIT 15"
            else:
                query = "SELECT p.num, profileImage, height, weight, viewCount, pickCount, cViewCount, ui.name, ui.birth, ui.entertain," \
                        "       ui.gender, ui.military, ui.school, ui.major, talent, comment, mainYoutube, isCareer, '0' AS proPick " \
                        "FROM profile_info AS p LEFT JOIN user_info AS ui  ON p.userID = ui.userID " \
                        "     LEFT JOIN ( SELECT profileNum, COUNT(*) AS career FROM profile_career WHERE title LIKE '%" + search + "%' OR `role` LIKE '%" + search + "%' ) AS c ON p.num = c.profileNum " \
                        "     LEFT JOIN ( SELECT profileNum, COUNT(*) AS etcCareer FROM profile_etccareer WHERE title LIKE '%" + search + "%' OR `role` LIKE '%" + search + "%' ) AS d ON p.num = d.profileNum " \
                        "WHERE public = '0' and isDelete = '0' and  " \
                        "      ( career > 0 OR etcCareer > 0 OR `foreign` LIKE '%" + search + "%' OR talent LIKE '%" + search + "' OR `comment` LIKE '%" + search + "%' OR `careerYear` LIKE '%" + search + "%' OR `careerMonth` LIKE '%" + search + "%' " \
                        "        OR `foreign` LIKE '%" + search + "%' OR `birth` LIKE '%" + search + "%' OR `finalSchool` LIKE '%" + search + "%' OR `school` LIKE '%" + search + "%' OR `major` LIKE '%" + search + "%' OR `entertain` LIKE '%" + search + "%' OR `military` LIKE '%" + search + "%')  " \
                        "ORDER BY regDate DESC  " \
                        "LIMIT 15"

        result = cursor.execute(query)
        searching = cursor.fetchall()

        connection.commit()
        connection.close()

        return render(request, 'picktalk/search.html', {"cateType": cateType, "searching": searching, "search":search })

def notice(request, num) :
    notice = QaNotice.objects.get(num=num)

    image = ""
    if notice.image != "" and notice.image != None :
        image = notice.image.split("|")

    return render(request, 'picktalk/notice.html', {"notice": notice, "image" : image})


def notiList(request, page) :

    block = 10
    start = (page - 1) * block
    end = page * block

    noti = QaNotice.objects.all()
    notice = noti.order_by("-regdate")[start:end]

    allPage = ( noti.count() / block ) + 1

    paging = getPageList( page, allPage )

    return render(request, 'picktalk/notiList.html', {"notice": notice, "paging" : paging, "page":page})


def proList(request, type, page, num) :

    block = 10
    start = (page - 1) * block
    end = page * block

    cursor = connection.cursor()
    user = request.session.get('id', '')

    if type == "audi" :
        query = "SELECT  p.num, profileImage, height, weight, viewCount, pickCount, cViewCount, ui.name, ui.birth, ui.entertain, ui.gender, ui.military, ui.school, ui.major, talent, p.COMMENT, mainYoutube, isCareer " \
                "FROM audition_apply AS audi LEFT JOIN profile_info AS p ON audi.profileNum = p.num " \
                "      LEFT JOIN user_info AS ui ON p.userID  = ui.userID " \
                "WHERE audi.auditionNum = '"+num+"' " \
                "order by audi.regTime desc limit "+ str(start) + ", " + str(end)

    elif type == "pick" :
        query = "SELECT  p.num, profileImage, height, weight, viewCount, pickCount, cViewCount, ui.name, ui.birth, ui.entertain, ui.gender, ui.military, ui.school, ui.major, talent, COMMENT, mainYoutube, isCareer " \
                "FROM profile_pick AS pp LEFT JOIN profile_info AS p ON pp.profileNum = p.num " \
                "     LEFT JOIN user_info AS ui ON p.userID  = ui.userID  " \
                "WHERE pp.userID = '"+user+"'  and p.isDelete = '0' " \
                "order by pp.regTime desc  limit "+ str(start) + ", " + str(end)

    elif type == "suggest" :
        query = "SELECT p.num, profileImage, height, weight, ui.name, ui.birth, ui.entertain, ui.gender, ui.military, ui.school, ui.major, talent, ps.COMMENT " \
                "FROM profile_suggest AS ps LEFT JOIN profile_info AS p ON ps.profileNum = p.num " \
                "     LEFT JOIN user_info AS ui ON ps.userID  = ui.userID  " \
                "WHERE ps.suUserID = '" + user + "' and p.isDelete = '0' " \
                "order by ps.regTime desc limit "+ str(start) + ", " + str(end)

    result = cursor.execute(query)
    profile = cursor.fetchall()

    connection.commit()
    connection.close()

    return render(request, 'user/proList.html', {"type": type, "page":page, "profile": profile,
                                                 "allCount" : cursor.rowcount })

def getPageList ( nowPage, allPage) :

    sPage = nowPage - 2
    if sPage <= 0 :
        startPage = 1
    elif sPage + 4 > allPage :
        startPage = allPage - 4
    else :
        startPage = sPage

    ePage = 1
    if allPage < 5 :
        ePage = allPage
    elif startPage + 4 > allPage :
        ePage = allPage
    else :
        ePage = startPage + 4

    paging = list(range(int(startPage), int(ePage)+1))

    return paging