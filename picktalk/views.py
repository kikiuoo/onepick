import smtplib
from django.db.models import Subquery
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import  loader
from django.db import connection
from django.utils import timezone
from django.http import JsonResponse
from email.mime.text import MIMEText
import socket
from requests import get
import time

from picktalk.models import *

from myonepick.common import *

# Create your views here.

# Index 페이지 Query 내용
def index(request):
    user = request.session.get('id', '')

    nowTime = timezone.now()
    if user:
        # 메인 진입시 회원정보 누락시 회원가입 페이지 이동.
        isUser = UserInfo.objects.get(userid=user)

        if (isUser.phone == None or isUser.email == None or isUser.name == None or isUser.usertype == "S-NORMAL"  \
            or isUser.phone == "" or isUser.email == "" or isUser.name == ""):
            returnUrl = "/users/join/" + str(user) + "/oldUser/"

            return redirect(returnUrl)
        elif isUser.phone == None or isUser.email == None or isUser.name == None or isUser.usertype == "S-NORMAL" \
                or isUser.phone == "" or isUser.email == "" or isUser.name == "" :
            returnUrl = "/users/join/" + str(user) + "/social/"

            return redirect(returnUrl)

    try :
        cursor = connection.cursor()

        # 메인 베너
        query = "SELECT * FROM banner_info WHERE viewType = 'main' and nowView = '1' AND startTime <= NOW() AND endTime >= NOW() "
        result = cursor.execute(query)
        mainbanner = cursor.fetchall()

        if user :
            query = "SELECT AI.num, AI.title, AI.endDate, AI.ordinary, UC.logoImage, (SELECT COUNT(*) FROM audition_pick WHERE userID = '" + user +"' AND auditionNum = AI.num ) AS audiPick " \
                    "FROM audition_recommend as ar left join audition_info AS AI ON ar.auditionNum = AI.num  " \
                    "LEFT JOIN user_company AS UC ON AI.userID  = UC.userID " \
                    "where (AI.isDelete = '0' or AI.isDelete is null ) and disType = 'main' " \
                    "order by ar.disOrder asc "
        else :
            query = "SELECT AI.num, AI.title, AI.endDate, AI.ordinary, UC.logoImage, '0' AS audiPick " \
                    "FROM audition_recommend as ar left join audition_info AS AI ON ar.auditionNum = AI.num  " \
                    "LEFT JOIN user_company AS UC ON AI.userID  = UC.userID " \
                    "where (AI.isDelete = '0' or AI.isDelete is null ) and disType = 'main' " \
                    "order by ar.disOrder asc "

        result = cursor.execute(query)
        auditions = cursor.fetchall()

        # 프로필 최신
        if user:
            query = "SELECT p.num, profileImage, height, weight, ui.name, ui.birth, ui.entertain, ui.military, (SELECT COUNT(*) FROM profile_pick WHERE userID = '" + user +"' AND profileNum = p.num ) AS proPick " \
                    "FROM profile_info AS p LEFT JOIN user_info AS ui  ON p.userID = ui.userID " \
                    "WHERE public = '0' and isDelete = '0' and ui.userID != '' and ui.name is not null and ui.name != ''  " \
                    "ORDER BY regDate DESC  " \
                    "LIMIT 4"
        else:
            query = "SELECT p.num, profileImage, height, weight, ui.name, ui.birth, ui.entertain, ui.military, '0' AS proPick " \
                    "FROM profile_info AS p LEFT JOIN user_info AS ui " \
                    "     ON p.userID = ui.userID " \
                    "WHERE public = '0' and isDelete = '0' and ui.userID != '' and ui.name is not null and ui.name != ''  " \
                    "ORDER BY  regDate DESC   " \
                    "LIMIT 4"

        result = cursor.execute(query)
        newProfile = cursor.fetchall()

        # 프로필 추천
        if user:
            query = "SELECT PI.num, profileImage, height, weight, ui.name, ui.birth, ui.entertain, ui.military, (SELECT COUNT(*) FROM profile_pick WHERE userID = '" + user +"' AND profileNum = PI.num ) AS proPick " \
                    "FROM profile_recommend AS PR LEFT JOIN profile_info AS PI ON PR.profileNum = PI.num " \
                    "     LEFT JOIN user_info AS ui ON PI.userID = ui.userID " \
                    "where ui.name is not null and ui.name != '' " \
                    "ORDER BY RAND() LIMIT 4"
        else:
            query = "SELECT PI.num, profileImage, height, weight, ui.name, ui.birth, ui.entertain, ui.military, '0' AS proPick " \
                    "FROM profile_recommend AS PR LEFT JOIN profile_info AS PI ON PR.profileNum = PI.num " \
                    "     LEFT JOIN user_info AS ui ON PI.userID = ui.userID " \
                    "where ui.name is not null and ui.name != '' " \
                    "ORDER BY RAND() LIMIT 4"

        result = cursor.execute(query)
        recomProfile = cursor.fetchall()



        # 프로필 베스트
        # 0,1,2,3,12,13,14,15  -- 주간베스트 ( 주 best 30명 랜덤 )
        # 4,5,6,7,16,17,18,19  -- 월간베스트 ( 월 best 50명 랜덤 )
        # 8,9,10,11,20,21,22,23  -- 전체 베스트 ( view 수 1000이 넘는 사람 랜덤 )
        now = time
        nowTimes = now.localtime().tm_hour

        #주간 베스트
        if nowTimes == 0 or  nowTimes == 1 or  nowTimes == 2 or  nowTimes == 3 or nowTimes == 12 or  nowTimes == 13 or  nowTimes == 14 or nowTimes == 15 :
            if user:
                query = "SELECT PI.num, profileImage, height, weight, ui.name, ui.birth, ui.entertain, ui.military, (SELECT COUNT(*) FROM profile_pick WHERE userID = '" + user +"' AND profileNum = PI.num ) AS proPick " \
                        "FROM ( SELECT profileNum, COUNT(*) AS views " \
                        "    	FROM profile_view " \
                        "   	WHERE regTime BETWEEN DATE_ADD(NOW(),INTERVAL -1 WEEK ) AND NOW() " \
                        "   	GROUP BY profileNum " \
                        "   	ORDER BY views DESC LIMIT 30 ) A  LEFT JOIN profile_info AS PI ON A.profileNum = PI.num " \
                        "     LEFT JOIN user_info AS ui ON PI.userID = ui.userID " \
                        "where ui.name is not null and ui.name != '' " \
                        "ORDER BY RAND() LIMIT 4"

            else:
                query = "SELECT PI.num, profileImage, height, weight, ui.name, ui.birth, ui.entertain, ui.military, '0' AS proPick " \
                        "FROM ( SELECT profileNum, COUNT(*) AS views " \
                        "    	FROM profile_view " \
                        "   	WHERE regTime BETWEEN DATE_ADD(NOW(),INTERVAL -1 WEEK ) AND NOW() " \
                        "   	GROUP BY profileNum " \
                        "   	ORDER BY views DESC LIMIT 30 ) A  LEFT JOIN profile_info AS PI ON A.profileNum = PI.num " \
                        "     LEFT JOIN user_info AS ui ON PI.userID = ui.userID " \
                        "where ui.name is not null and ui.name != '' " \
                        "ORDER BY RAND() LIMIT 4"


        # 월간 베스트 4,5,6,7,16,17,18,19
        elif nowTimes == 4 or  nowTimes == 5 or  nowTimes == 6 or  nowTimes == 7 or nowTimes == 16 or  nowTimes == 17 or  nowTimes == 18 or nowTimes == 19 :
            if user:
                query = "SELECT PI.num, profileImage, height, weight, ui.name, ui.birth, ui.entertain, ui.military, (SELECT COUNT(*) FROM profile_pick WHERE userID = '" + user +"' AND profileNum = PI.num ) AS proPick " \
                        "FROM ( SELECT profileNum, COUNT(*) AS views " \
                        "    	FROM profile_view " \
                        "   	WHERE regTime BETWEEN DATE_ADD(NOW(),INTERVAL -1 MONTH ) AND NOW() " \
                        "   	GROUP BY profileNum " \
                        "   	ORDER BY views DESC LIMIT 50 ) A  LEFT JOIN profile_info AS PI ON A.profileNum = PI.num " \
                        "     LEFT JOIN user_info AS ui ON PI.userID = ui.userID " \
                        "where ui.name is not null and ui.name != '' " \
                        "ORDER BY RAND() LIMIT 4"

            else:
                query = "SELECT PI.num, profileImage, height, weight, ui.name, ui.birth, ui.entertain, ui.military, '0' AS proPick " \
                        "FROM ( SELECT profileNum, COUNT(*) AS views " \
                        "    	FROM profile_view " \
                        "   	WHERE regTime BETWEEN DATE_ADD(NOW(),INTERVAL -1 MONTH ) AND NOW() " \
                        "   	GROUP BY profileNum " \
                        "   	ORDER BY views DESC LIMIT 50 ) A  LEFT JOIN profile_info AS PI ON A.profileNum = PI.num " \
                        "     LEFT JOIN user_info AS ui ON PI.userID = ui.userID " \
                        "where ui.name is not null and ui.name != '' " \
                        "ORDER BY RAND() LIMIT 4"

        # 전체 베스트 8,9,10,11,20,21,22,23
        elif nowTimes == 8 or nowTimes == 9 or nowTimes == 10 or nowTimes == 11 or nowTimes == 20 or nowTimes == 21 or nowTimes == 22 or nowTimes == 23:
            if user:
                query = "SELECT PI.num, profileImage, height, weight, ui.name, ui.birth, ui.entertain, ui.military, (SELECT COUNT(*) FROM profile_pick WHERE userID = '" + user +"' AND profileNum = PI.num ) AS proPick " \
                        "FROM profile_info AS PI LEFT JOIN user_info AS ui  " \
                        "     ON PI.userID = ui. userID " \
                        "WHERE viewCount > 1000 and ui.name is not null and ui.name != '' " \
                        "ORDER BY RAND() LIMIT 4"
            else:
                query = "SELECT PI.num, profileImage, height, weight, ui.name, ui.birth, ui.entertain, ui.military, '0' AS proPick " \
                        "FROM profile_info AS PI LEFT JOIN user_info AS ui  " \
                        "     ON PI.userID = ui. userID " \
                        "WHERE viewCount > 1000 and ui.name is not null and ui.name != '' " \
                        "ORDER BY RAND() LIMIT 4"

        result = cursor.execute(query)
        bestProfile = cursor.fetchall()
        connection.commit()
        connection.close()

    except :
        print("error!")
        connection.rollback()

    return render(request, 'picktalk/index.html',
                  {'auditions': auditions, 'newProfile': newProfile , 'recomProfile' : recomProfile,
                   'bestProfile' : bestProfile, 'mainbanner' : mainbanner })


def downstime(request) :

    return render(request, 'picktalk/downstime.html')

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

    email = request.GET.get("email");
    title = request.GET.get("title");
    content = request.GET.get("content");

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
    try:
        cursor = connection.cursor()

        user = request.session.get('id', '')

        # 검색 결과 등록
        if page == 1 :
            nowTime = timezone.now()
            saveSearch = UserSearch.objects.create(userid=user, search=search, regdate=nowTime)

        block = 10
        start = (int(page) - 1) * block
        end = int(page) * block

        if cateType == "audition" :

            query = "SELECT * " \
                    "FROM audition_info AS ai LEFT JOIN cate_main AS cm ON ai.cate = cm.cateCode " \
                    "    LEFT JOIN  user_company AS uc ON ai.userID = uc.userID " \
                    "where ( ai.isDelete = '0' or ai.isDelete is null ) " \
                    "     and ( title LIKE '%" + search + "%' OR age LIKE '%" + search + "%' OR gender LIKE '%" + search + "%' OR career LIKE '%" + search + "%' OR essential LIKE '%" + search + "%'  OR preparation LIKE '%" + search + "%' ) " \
                    "ORDER BY ai.regTime DESC ";

            result = cursor.execute(query)
            allList = cursor.fetchall()

            if user:
                query = "SELECT ai.num, ai.title, cm.cateName, ai.career, ai.age, ai.endDate, ai.regTime, ai.ordinary, uc.logoImage, DATEDIFF(NOW(),  ai.regTime) AS diffDate, (SELECT COUNT(*) FROM audition_pick WHERE userID = '" + user + "' AND auditionNum = ai.num ) AS audiPick " \
                        "FROM audition_info AS ai LEFT JOIN cate_main AS cm ON ai.cate = cm.cateCode " \
                        "    LEFT JOIN  user_company AS uc ON ai.userID = uc.userID " \
                        "where ( ai.isDelete = '0' or ai.isDelete is null ) " \
                        "     and ( title LIKE '%" + search + "%' OR age LIKE '%" + search + "%' OR gender LIKE '%" + search + "%' OR career LIKE '%" + search + "%' OR essential LIKE '%" + search + "%'  OR preparation LIKE '%" + search + "%' ) " \
                        "ORDER BY ai.regTime DESC limit " + str(start) + ", " + str(block)
            else:
                query = "SELECT ai.num, ai.title, cm.cateName, ai.career, ai.age, ai.endDate, ai.regTime, ai.ordinary, uc.logoImage, DATEDIFF(NOW(),  ai.regTime) AS diffDate , '0' AS audiPick " \
                        "FROM audition_info AS ai LEFT JOIN cate_main AS cm ON ai.cate = cm.cateCode " \
                        "    LEFT JOIN  user_company AS uc ON ai.userID = uc.userID " \
                        "where ( ai.isDelete = '0' or ai.isDelete is null ) " \
                        "     and ( title LIKE '%" + search + "%' OR age LIKE '%" + search + "%' OR gender LIKE '%" + search + "%' OR career LIKE '%" + search + "%' OR essential LIKE '%" + search + "%'  OR preparation LIKE '%" + search + "%' ) " \
                        "ORDER BY ai.regTime DESC limit " + str(start) + ", " + str(block)

            result = cursor.execute(query)
            searching = cursor.fetchall()


        else :

            query = "SELECT * " \
                    "FROM profile_info AS p LEFT JOIN user_info AS ui  ON p.userID = ui.userID " \
                    "     LEFT JOIN ( SELECT profileNum, COUNT(*) AS career FROM profile_career WHERE title LIKE '%" + search + "%' OR `role` LIKE '%" + search + "%' group by profileNum ) AS c ON p.num = c.profileNum " \
                    "     LEFT JOIN ( SELECT profileNum, COUNT(*) AS etcCareer FROM profile_etccareer WHERE title LIKE '%" + search + "%' OR `role` LIKE '%" + search + "%' group by profileNum ) AS d ON p.num = d.profileNum " \
                    "WHERE public = '0' and isDelete = '0'  and ui.userID != '' and  " \
                    "      ( ui.name LIKE '%" + search + "%' OR career > 0 OR etcCareer > 0 OR `foreign` LIKE '%" + search + "%' OR talent LIKE '%" + search + "' OR `comment` LIKE '%" + search + "%' OR `careerYear` LIKE '%" + search + "%' OR `careerMonth` LIKE '%" + search + "%' " \
                    "        OR `foreign` LIKE '%" + search + "%' OR `birth` LIKE '%" + search + "%' OR `finalSchool` LIKE '%" + search + "%' OR `school` LIKE '%" + search + "%' OR `major` LIKE '%" + search + "%' OR `entertain` LIKE '%" + search + "%' OR `military` LIKE '%" + search + "%')  " \
                    "ORDER BY regDate DESC "

            print(query)

            result = cursor.execute(query)
            allList = cursor.fetchall()

            if user:
                query = "SELECT p.num , profileImage, height, weight, viewCount, pickCount, cViewCount, ui.name, ui.birth, ui.entertain, " \
                        "       ui.gender, ui.military, ui.school, ui.major, talent, comment, mainYoutube, isCareer, (SELECT COUNT(*) FROM profile_pick WHERE userID = '" + user + "' AND profileNum = p.num ) AS proPick " \
                        "FROM profile_info AS p LEFT JOIN user_info AS ui  ON p.userID = ui.userID " \
                        "     LEFT JOIN ( SELECT profileNum, COUNT(*) AS career FROM profile_career WHERE title LIKE '%" + search + "%' OR `role` LIKE '%" + search + "%' group by profileNum ) AS c ON p.num = c.profileNum " \
                        "     LEFT JOIN ( SELECT profileNum, COUNT(*) AS etcCareer FROM profile_etccareer WHERE title LIKE '%" + search + "%' OR `role` LIKE '%" + search + "%' group by profileNum ) AS d ON p.num = d.profileNum " \
                        "WHERE public = '0' and isDelete = '0'  and ui.userID != '' and  " \
                        "      ( ui.name LIKE '%" + search + "%' OR career > 0 OR etcCareer > 0 OR `foreign` LIKE '%" + search + "%' OR talent LIKE '%" + search + "' OR `comment` LIKE '%" + search + "%' OR `careerYear` LIKE '%" + search + "%' OR `careerMonth` LIKE '%" + search + "%' " \
                        "        OR `foreign` LIKE '%" + search + "%' OR `birth` LIKE '%" + search + "%' OR `finalSchool` LIKE '%" + search + "%' OR `school` LIKE '%" + search + "%' OR `major` LIKE '%" + search + "%' OR `entertain` LIKE '%" + search + "%' OR `military` LIKE '%" + search + "%')  " \
                        "ORDER BY regDate DESC " \
                        " LIMIT " + str(start) + ", " + str(block)
            else:
                query = "SELECT p.num, profileImage, height, weight, viewCount, pickCount, cViewCount, ui.name, ui.birth, ui.entertain," \
                        "       ui.gender, ui.military, ui.school, ui.major, talent, comment, mainYoutube, isCareer, '0' AS proPick " \
                        "FROM profile_info AS p LEFT JOIN user_info AS ui  ON p.userID = ui.userID " \
                        "     LEFT JOIN ( SELECT profileNum, COUNT(*) AS career FROM profile_career WHERE title LIKE '%" + search + "%' OR `role` LIKE '%" + search + "%' ) AS c ON p.num = c.profileNum " \
                        "     LEFT JOIN ( SELECT profileNum, COUNT(*) AS etcCareer FROM profile_etccareer WHERE title LIKE '%" + search + "%' OR `role` LIKE '%" + search + "%' ) AS d ON p.num = d.profileNum " \
                        "WHERE public = '0' and isDelete = '0'  and ui.userID != '' and  " \
                        "      ( ui.name LIKE '%" + search + "%' OR career > 0 OR etcCareer > 0 OR `foreign` LIKE '%" + search + "%' OR talent LIKE '%" + search + "' OR `comment` LIKE '%" + search + "%' OR `careerYear` LIKE '%" + search + "%' OR `careerMonth` LIKE '%" + search + "%' " \
                        "        OR `foreign` LIKE '%" + search + "%' OR `birth` LIKE '%" + search + "%' OR `finalSchool` LIKE '%" + search + "%' OR `school` LIKE '%" + search + "%' OR `major` LIKE '%" + search + "%' OR `entertain` LIKE '%" + search + "%' OR `military` LIKE '%" + search + "%')  " \
                        "ORDER BY regDate DESC  " \
                        " LIMIT " + str(start) + ", " + str(block)

            result = cursor.execute(query)
            searching = cursor.fetchall()

        connection.commit()
        connection.close()

        allPage = int(len(allList) / block) + 1
        paging = getPageList_v2(page, allPage)

    except:
        connection.rollback()

    return render(request, 'picktalk/search.html',
                  {"cateType": cateType, "searching": searching, "search":search, "paging":paging, "page" : page,
                   "leftPage" : page-1, "rightPage" : page+1, "lastPage" : allPage,"allList":len(allList)})




def getSearchProfile(request) :

    try :
        cursor = connection.cursor()

        page = request.GET['page']
        search = request.GET['word']

        page = int(page)

        user = request.session.get('id', '')
        block = 10
        start = (page - 1) * block
        end = page * block

        if user:
            query = "SELECT p.num , profileImage, height, weight, viewCount, pickCount, cViewCount, ui.name, ui.birth, ui.entertain, " \
                    "       ui.gender, ui.military, ui.school, ui.major, talent, comment, mainYoutube, isCareer, (SELECT COUNT(*) FROM profile_pick WHERE userID = '" + user + "' AND profileNum = p.num ) AS proPick " \
                    "FROM profile_info AS p LEFT JOIN user_info AS ui  ON p.userID = ui.userID " \
                    "     LEFT JOIN ( SELECT profileNum, COUNT(*) AS career FROM profile_career WHERE title LIKE '%" + search + "%' OR `role` LIKE '%" + search + "%' group by profileNum ) AS c ON p.num = c.profileNum " \
                    "     LEFT JOIN ( SELECT profileNum, COUNT(*) AS etcCareer FROM profile_etccareer WHERE title LIKE '%" + search + "%' OR `role` LIKE '%" + search + "%' group by profileNum ) AS d ON p.num = d.profileNum " \
                    "WHERE public = '0' and isDelete = '0'  and ui.userID != '' and  " \
                    "      ( ui.name LIKE '%" + search + "%' OR  career > 0 OR etcCareer > 0 OR `foreign` LIKE '%" + search + "%' OR talent LIKE '%" + search + "' OR `comment` LIKE '%" + search + "%' OR `careerYear` LIKE '%" + search + "%' OR `careerMonth` LIKE '%" + search + "%' " \
                    "        OR `foreign` LIKE '%" + search + "%' OR `birth` LIKE '%" + search + "%' OR `finalSchool` LIKE '%" + search + "%' OR `school` LIKE '%" + search + "%' OR `major` LIKE '%" + search + "%' OR `entertain` LIKE '%" + search + "%' OR `military` LIKE '%" + search + "%')  " \
                    "ORDER BY regDate DESC " \
                    " LIMIT " + str(start) + ", " + str(block)

        else:
            query = "SELECT p.num, profileImage, height, weight, viewCount, pickCount, cViewCount, ui.name, ui.birth, ui.entertain," \
                    "       ui.gender, ui.military, ui.school, ui.major, talent, comment, mainYoutube, isCareer, '0' AS proPick " \
                    "FROM profile_info AS p LEFT JOIN user_info AS ui  ON p.userID = ui.userID " \
                    "     LEFT JOIN ( SELECT profileNum, COUNT(*) AS career FROM profile_career WHERE title LIKE '%" + search + "%' OR `role` LIKE '%" + search + "%' ) AS c ON p.num = c.profileNum " \
                    "     LEFT JOIN ( SELECT profileNum, COUNT(*) AS etcCareer FROM profile_etccareer WHERE title LIKE '%" + search + "%' OR `role` LIKE '%" + search + "%' ) AS d ON p.num = d.profileNum " \
                    "WHERE public = '0' and isDelete = '0'  and ui.userID != '' and  " \
                    "      ( ui.name LIKE '%" + search + "%' OR career > 0 OR etcCareer > 0 OR `foreign` LIKE '%" + search + "%' OR talent LIKE '%" + search + "' OR `comment` LIKE '%" + search + "%' OR `careerYear` LIKE '%" + search + "%' OR `careerMonth` LIKE '%" + search + "%' " \
                    "        OR `foreign` LIKE '%" + search + "%' OR `birth` LIKE '%" + search + "%' OR `finalSchool` LIKE '%" + search + "%' OR `school` LIKE '%" + search + "%' OR `major` LIKE '%" + search + "%' OR `entertain` LIKE '%" + search + "%' OR `military` LIKE '%" + search + "%')  " \
                    "ORDER BY regDate DESC  " \
                    " LIMIT " + str(start) + ", " + str(block)

        result = cursor.execute(query)
        searching = cursor.fetchall()

        connection.commit()
        connection.close()

    except:
        connection.rollback()

    return render(request, 'profiles/ajax_profileList.html', {'profiles':searching})


def proList(request, type, page, num, filter) :

    block = 10
    start = (page - 1) * block
    end = page * block

    cursor = connection.cursor()
    user = request.session.get('id', '')

    if type == "audi":

        addWhere = ""
        if filter == "pass" :
            addWhere = " and pick = 'Y' "

        query = "SELECT profileNum, regTime FROM audition_apply WHERE auditionNum = '" + num + "' "+addWhere+" GROUP BY profileNum ORDER BY regTime DESC "

        result = cursor.execute(query)
        allList = cursor.fetchall()

        if user:
            query = "SELECT  p.num, profileImage, height, weight, viewCount, pickCount, cViewCount, ui.name, ui.birth, ui.entertain, ui.gender, ui.military, ui.school, ui.major, talent, p.COMMENT, mainYoutube, isCareer, (SELECT COUNT(*) FROM profile_pick WHERE userID = '" + user + "' AND profileNum = p.num ) AS proPick, audi.COMMENT, audi.pick  " \
                    "FROM ( SELECT profileNum, COMMENT, pick,  regTime FROM audition_apply WHERE auditionNum = '" + num + "' "+addWhere+" GROUP BY profileNum ORDER BY regTime DESC ) AS audi " \
                    "LEFT JOIN profile_info AS p ON audi.profileNum = p.num " \
                    "      LEFT JOIN user_info AS ui ON p.userID  = ui.userID " \
                    "order by audi.regTime desc limit " + str(start) + ", " + str(block)

        else:
            query = "SELECT  p.num, profileImage, height, weight, viewCount, pickCount, cViewCount, ui.name, ui.birth, ui.entertain, ui.gender, ui.military, ui.school, ui.major, talent, p.COMMENT, mainYoutube, isCaree, '0' AS proPickr, audi.COMMENT, audi.pick  " \
                    "FROM ( SELECT profileNum, COMMENT, pick,  regTime FROM audition_apply WHERE auditionNum = '" + num + "' "+addWhere+" GROUP BY profileNum ORDER BY regTime DESC ) AS audi " \
                    "LEFT JOIN profile_info AS p ON audi.profileNum = p.num " \
                    "      LEFT JOIN user_info AS ui ON p.userID  = ui.userID " \
                    "order by audi.regTime desc limit " + str( start) + ", " + str(block)

    elif type == "pick":

        query = "SELECT  p.num, profileImage, height, weight, viewCount, pickCount, cViewCount, ui.name, ui.birth, ui.entertain, ui.gender, ui.military, ui.school, ui.major, talent, COMMENT, mainYoutube, isCareer, '0' AS proPick " \
                "FROM profile_pick AS pp LEFT JOIN profile_info AS p ON pp.profileNum = p.num " \
                "     LEFT JOIN user_info AS ui ON p.userID  = ui.userID  " \
                "WHERE pp.userID = '" + user + "'  and p.isDelete = '0' "

        result = cursor.execute(query)
        allList = cursor.fetchall()

        if user:
            query = "SELECT  p.num, profileImage, height, weight, viewCount, pickCount, cViewCount, ui.name, ui.birth, ui.entertain, ui.gender, ui.military, ui.school, ui.major, talent, COMMENT, mainYoutube, isCareer, (SELECT COUNT(*) FROM profile_pick WHERE userID = '" + user + "' AND profileNum = p.num ) AS proPick  " \
                    "FROM profile_pick AS pp LEFT JOIN profile_info AS p ON pp.profileNum = p.num " \
                    "     LEFT JOIN user_info AS ui ON p.userID  = ui.userID  " \
                    "WHERE pp.userID = '" + user + "'  and p.isDelete = '0' " \
                    "order by pp.regTime desc  limit " + str(start) + ", " + str(block)

        else:
            query = "SELECT  p.num, profileImage, height, weight, viewCount, pickCount, cViewCount, ui.name, ui.birth, ui.entertain, ui.gender, ui.military, ui.school, ui.major, talent, COMMENT, mainYoutube, isCareer, '0' AS proPick " \
                    "FROM profile_pick AS pp LEFT JOIN profile_info AS p ON pp.profileNum = p.num " \
                    "     LEFT JOIN user_info AS ui ON p.userID  = ui.userID  " \
                    "WHERE pp.userID = '" + user + "'  and p.isDelete = '0' " \
                    "order by pp.regTime desc  limit " + str(start) + ", " + str(block)

    elif type == "suggest":

        query = "SELECT p.num, profileImage, height, weight, ui.name, ui.birth, ui.entertain, ui.gender, ui.military, ui.school, ui.major, talent, ps.COMMENT, '0' AS proPick " \
                "FROM profile_suggest AS ps LEFT JOIN profile_info AS p ON ps.profileNum = p.num " \
                "     LEFT JOIN user_info AS ui ON ps.userID  = ui.userID  " \
                "WHERE ps.suUserID = '" + user + "' and p.isDelete = '0' "

        result = cursor.execute(query)
        allList = cursor.fetchall()


        if user:
            query = "SELECT p.num, profileImage, height, weight, ui.name, ui.birth, ui.entertain, ui.gender, ui.military, ui.school, ui.major, talent, ps.COMMENT, (SELECT COUNT(*) FROM profile_pick WHERE userID = '" + user + "' AND profileNum = p.num ) AS proPick  " \
            "FROM profile_suggest AS ps LEFT JOIN profile_info AS p ON ps.profileNum = p.num " \
            "     LEFT JOIN user_info AS ui ON ps.userID  = ui.userID  " \
            "WHERE ps.suUserID = '" + user + "' and p.isDelete = '0' " \
            "order by ps.regTime desc limit " + str(start) + ", " + str(block)

        else :
            query = "SELECT p.num, profileImage, height, weight, ui.name, ui.birth, ui.entertain, ui.gender, ui.military, ui.school, ui.major, talent, ps.COMMENT, '0' AS proPick " \
                    "FROM profile_suggest AS ps LEFT JOIN profile_info AS p ON ps.profileNum = p.num " \
                    "     LEFT JOIN user_info AS ui ON ps.userID  = ui.userID  " \
                    "WHERE ps.suUserID = '" + user + "' and p.isDelete = '0' " \
                    "order by ps.regTime desc limit "+ str(start) + ", " + str(block)

    result = cursor.execute(query)
    profile = cursor.fetchall()

    allPage = int(len(allList) / block) + 1
    paging = getPageList_v2(page, allPage)

    connection.commit()
    connection.close()

    return render(request, 'user/proList.html',
                  {"type": type, "profile": profile, "filter" : filter, "paging":paging, "page": page,
                   "leftPage": page - 1, "rightPage": page + 1, "lastPage": allPage,
                   "allCount" : cursor.rowcount, "allList" : len(allList), "num": num })

def proList2(request, type, page, num, filter) :

    block = 10
    start = (page - 1) * block
    end = page * block

    cursor = connection.cursor()
    user = request.session.get('id', '')

    if type == "audi":

        addWhere = ""
        if filter == "pass":
            addWhere = " and pick = 'Y' "

        if user:
            query = "SELECT  p.num, profileImage, height, weight, viewCount, pickCount, cViewCount, ui.name, ui.birth, ui.entertain, ui.gender, ui.military, ui.school, ui.major, talent, p.COMMENT, mainYoutube, isCareer, (SELECT COUNT(*) FROM profile_pick WHERE userID = '" + user + "' AND profileNum = p.num ) AS proPick, audi.COMMENT, audi.pick  " \
                    "FROM ( SELECT profileNum, COMMENT, pick,  regTime FROM audition_apply WHERE auditionNum = '" + num + "' "+addWhere+" GROUP BY profileNum ORDER BY regTime DESC ) AS audi " \
                    "LEFT JOIN profile_info AS p ON audi.profileNum = p.num " \
                    "      LEFT JOIN user_info AS ui ON p.userID  = ui.userID " \
                    "order by audi.regTime desc limit " + str(start) + ", " + str(block)

        else:
            query = "SELECT  p.num, profileImage, height, weight, viewCount, pickCount, cViewCount, ui.name, ui.birth, ui.entertain, ui.gender, ui.military, ui.school, ui.major, talent, p.COMMENT, mainYoutube, isCaree, '0' AS proPickr, audi.COMMENT, audi.pick  " \
                    "FROM ( SELECT profileNum, COMMENT, pick,  regTime FROM audition_apply WHERE auditionNum = '" + num + "' "+addWhere+" GROUP BY profileNum ORDER BY regTime DESC ) AS audi " \
                    "LEFT JOIN profile_info AS p ON audi.profileNum = p.num " \
                    "      LEFT JOIN user_info AS ui ON p.userID  = ui.userID " \
                    "order by audi.regTime desc limit " + str( start) + ", " + str(block)


    elif type == "pick":

        if user:
            query = "SELECT  p.num, profileImage, height, weight, viewCount, pickCount, cViewCount, ui.name, ui.birth, ui.entertain, ui.gender, ui.military, ui.school, ui.major, talent, COMMENT, mainYoutube, isCareer, (SELECT COUNT(*) FROM profile_pick WHERE userID = '" + user + "' AND profileNum = p.num ) AS proPick  " \
                    "FROM profile_pick AS pp LEFT JOIN profile_info AS p ON pp.profileNum = p.num " \
                    "     LEFT JOIN user_info AS ui ON p.userID  = ui.userID  " \
                    "WHERE pp.userID = '" + user + "'  and p.isDelete = '0' " \
                    "order by pp.regTime desc  limit " + str(start) + ", " + str(block)

        else:
            query = "SELECT  p.num, profileImage, height, weight, viewCount, pickCount, cViewCount, ui.name, ui.birth, ui.entertain, ui.gender, ui.military, ui.school, ui.major, talent, COMMENT, mainYoutube, isCareer, '0' AS proPick " \
                    "FROM profile_pick AS pp LEFT JOIN profile_info AS p ON pp.profileNum = p.num " \
                    "     LEFT JOIN user_info AS ui ON p.userID  = ui.userID  " \
                    "WHERE pp.userID = '" + user + "'  and p.isDelete = '0' " \
                    "order by pp.regTime desc  limit " + str(start) + ", " + str(block)

    elif type == "suggest":

        if user:
            query = "SELECT p.num, profileImage, height, weight, ui.name, ui.birth, ui.entertain, ui.gender, ui.military, ui.school, ui.major, talent, ps.COMMENT, (SELECT COUNT(*) FROM profile_pick WHERE userID = '" + user + "' AND profileNum = p.num ) AS proPick  " \
            "FROM profile_suggest AS ps LEFT JOIN profile_info AS p ON ps.profileNum = p.num " \
            "     LEFT JOIN user_info AS ui ON ps.userID  = ui.userID  " \
            "WHERE ps.suUserID = '" + user + "' and p.isDelete = '0' " \
            "order by ps.regTime desc limit " + str(start) + ", " + str(block)

        else :
            query = "SELECT p.num, profileImage, height, weight, ui.name, ui.birth, ui.entertain, ui.gender, ui.military, ui.school, ui.major, talent, ps.COMMENT, '0' AS proPick " \
                    "FROM profile_suggest AS ps LEFT JOIN profile_info AS p ON ps.profileNum = p.num " \
                    "     LEFT JOIN user_info AS ui ON ps.userID  = ui.userID  " \
                    "WHERE ps.suUserID = '" + user + "' and p.isDelete = '0' " \
                    "order by ps.regTime desc limit "+ str(start) + ", " + str(block)

    result = cursor.execute(query)
    profile = cursor.fetchall()

    print(profile)

    connection.commit()
    connection.close()

    return render(request, 'user/ajax_proList.html', {"type": type, "page":page, "profile": profile,"num": num })



def applyList(request, num) :

    page = request.GET.get("page", "1")
    page = int(page)

    filter = request.GET.get("listView", "all")

    nationality = request.GET.get('nationality', "")
    geneder = request.GET.get('geneder', "")
    military = request.GET.get('military', "")

    ageRadio = request.GET.get('ageRadio', "")
    age1 = request.GET.get('age1', "")
    age2 = request.GET.get('age2', "")

    heightRadio = request.GET.get('heightRadio', "")
    height1 = request.GET.get('height1', "")
    height2 = request.GET.get('height2', "")

    careerRadio = request.GET.get('careerRadio', "")
    career1 = request.GET.get('career1', "")
    career2 = request.GET.get('career2', "")

    foreSpec = request.GET.get('foreSpec', "")
    findSpec = request.GET.get('findSpec', "")
    tagSpec = request.GET.get('tagSpec', "")
    school = request.GET.get('school', "")

    block = 10
    start = (page - 1) * block
    end = page * block

    cursor = connection.cursor()
    user = request.session.get('id', '')


    # 검색 조건

    where = ""
    if nationality != "":
        where = where + " and nationality='" + nationality + "'"

    if military != "":
        where = where + " and military='" + military + "'"

    if geneder != "":
        where = where + " and gender='" + geneder + "'"

    if ageRadio != "":
        nowTime = str(timezone.now())
        year = nowTime.split('-')
        if ageRadio == "1":
            year10 = int(year[0]) - 9
            where = where + " and birth >= '" + str(year10) + "-12-31' "
        else:
            yearsOver = int(year[0]) - int(ageRadio) + 1
            where = where + " and birth <= '" + str(yearsOver) + "-12-31' "
    elif age1 != "" and age2 != "":
        nowTime = str(timezone.now())
        year = nowTime.split('-')
        age_1 = int(year[0]) - int(age1) + 1
        age_2 = int(year[0]) - int(age2) + 1
        where = where + " and birth >= '" + str(age_1) + "-01-01' and birth <= '" + str(age_2) + "-12-31' "
    elif age1 != "" or age2 != "":
        age1 = ""
        age2 = ""

    if heightRadio != "":
        where = where + " and height >= '" + heightRadio + "' "
    elif height1 != "" and height2 != "":
        where = where + " and height >= '" + str(height1) + "' and height <= '" + str(height2) + "' "
    elif height1 != "" or height2 != "":
        height1 = ""
        height2 = ""

    if careerRadio != "":
        if careerRadio == "0":
            where = where + " and ( careerYear < '1' or careerYear is null ) "
        else:
            where = where + " and careerYear >= '" + str(careerRadio) + "' "
    elif career1 != "" and career2 != "":
        where = where + " and careerYear >= '" + str(career1) + "' and careerYear <= '" + str(career2) + "'"
    elif career1 != "" or career2 != "":
        career1 = ""
        career2 = ""

    if foreSpec != "":
        foreign = foreSpec.split("|")

        where = where + " and ( "
        count = 0
        for fore in foreign:
            count = count + 1
            if count == 1:
                where = where + " `foreign` like '%" + fore + "%' "
            else:
                where = where + " or `foreign` like '%" + fore + "%' "

        where = where + " ) "

    else:
        foreign = ""

    if findSpec != "":
        specList = findSpec.split("|")

        where = where + " and ( "
        count = 0
        for spec in specList:
            count = count + 1
            specDetail = spec.split("$")
            if count == 1:
                where = where + " talent like '%" + specDetail[1] + "%' "
            else:
                where = where + " or talent like '%" + specDetail[1] + "%' "

        where = where + " ) "

    else:
        specList = ""

    if tagSpec != "":
        tagSpecList = tagSpec.split("|")

        where = where + " and ( "
        count = 0
        for tag in tagSpecList:
            count = count + 1
            if count == 1:
                where = where + " tag like '%" + tag + "%' "
            else:
                where = where + " or tag like '%" + tag + "%' "
        where = where + " ) "
    else:
        tagSpecList = ""

    if school != "":
        where = where + " and school like '%" + school + "%'"

    if filter == "pass":
        where = where + " and pick = 'Y' "

    query = "SELECT  *  " \
            "FROM ( SELECT profileNum, COMMENT, pick,  regTime FROM audition_apply WHERE auditionNum = '" + num + "' GROUP BY profileNum ORDER BY regTime DESC ) AS audi " \
            "LEFT JOIN profile_info AS p ON audi.profileNum = p.num " \
            "      LEFT JOIN user_info AS ui ON p.userID  = ui.userID " \
            "where 1 " + where + " " \
            "order by audi.regTime desc "

    result = cursor.execute(query)
    allList = cursor.fetchall()

    if user:
        query = "SELECT  p.num, profileImage, height, weight, viewCount, pickCount, cViewCount, ui.name, ui.birth, ui.entertain, ui.gender, ui.military, ui.school, ui.major, talent, p.COMMENT, mainYoutube, isCareer, (SELECT COUNT(*) FROM profile_pick WHERE userID = '" + user + "' AND profileNum = p.num ) AS proPick, audi.COMMENT, audi.pick  " \
                "FROM ( SELECT profileNum, COMMENT, pick,  regTime FROM audition_apply WHERE auditionNum = '" + num + "'  GROUP BY profileNum ORDER BY regTime DESC ) AS audi " \
                "LEFT JOIN profile_info AS p ON audi.profileNum = p.num " \
                "      LEFT JOIN user_info AS ui ON p.userID  = ui.userID " \
                "where 1 " + where + " " \
                "order by audi.regTime desc limit " + str(start) + ", " + str(block)

    else:
        query = "SELECT  p.num, profileImage, height, weight, viewCount, pickCount, cViewCount, ui.name, ui.birth, ui.entertain, ui.gender, ui.military, ui.school, ui.major, talent, p.COMMENT, mainYoutube, isCaree, '0' AS proPickr, audi.COMMENT, audi.pick  " \
                "FROM ( SELECT profileNum, COMMENT, pick,  regTime FROM audition_apply WHERE auditionNum = '" + num + "'  GROUP BY profileNum ORDER BY regTime DESC ) AS audi " \
                "LEFT JOIN profile_info AS p ON audi.profileNum = p.num " \
                "      LEFT JOIN user_info AS ui ON p.userID  = ui.userID " \
                "where 1 " + where + " " \
                "order by audi.regTime desc limit " + str(start) + ", " + str(block)

    result = cursor.execute(query)
    profile = cursor.fetchall()

    allPage = int(len(allList) / block) + 1
    paging = getPageList_v2(page, allPage)

    query = "SELECT * FROM profile_specialty GROUP BY `class` ORDER BY num ASC"

    result = cursor.execute(query)
    specialty = cursor.fetchall()

    tagList = ProfileTag.objects.all().order_by("tag")

    connection.commit()
    connection.close()

    return render(request, 'user/proList_apply.html',
                  {"profile": profile, "filter" : filter, "paging":paging, "page": page,
                   "leftPage": page - 1, "rightPage": page + 1, "lastPage": allPage,"allCount" : cursor.rowcount, "allList" : len(allList), "num": num,
                   "nationality":nationality, "geneder": geneder, "military": military, "ageRadio": ageRadio
                  , "age1": age1, "age2": age2, "school": school, "heightRadio": heightRadio, "height1": height1, "height2": height2
                  , "careerRadio": careerRadio, "career1": career1, "career2": career2, "foreSpec": foreSpec, "findSpec": findSpec, "tagSpec": tagSpec,
                  "foreList": foreign, "spList": specList, "tagSpecList": tagSpecList, "speList": specialty, "tagList": tagList })



def gsdv(request) :

    return render(request, 'picktalk/gsdv.txt')

def updateApplyPick(request) :

    pick = request.GET["pick"]
    auditionNum = request.GET["auditionNum"]
    profileNum = request.GET["profileNum"]
    comment = request.GET["comment"]

    apply = AuditionApply.objects.filter(auditionnum=auditionNum, profilenum=profileNum)

    for data in apply :
        data.pick = pick
        data.comment = comment

        data.save()

    return JsonResponse({"code": "0"})

def updateCounting(request) :

    user = request.session.get('id', '')

    ip = request.GET["ip"]
    device = request.GET["device"]
    nowTime = timezone.now()

    if user == "" :
        type = "ip"
        uKey = ip
    else :
        type = "id"
        uKey = user

    counting = UserCount.objects.create(type=type, ukey=uKey, device=device, regdate=nowTime)

    return JsonResponse({"code": "0"})


def updateBannerCount(request) :

    num = request.GET["num"]

    counting = BannerInfo.objects.get(num=num)
    counting.clickcount = counting.clickcount + 1
    counting.save()

    return JsonResponse({"code": "0"})
