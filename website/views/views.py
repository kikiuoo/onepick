import smtplib
from django.shortcuts import render, redirect
from django.db import connection
from django.utils import timezone
from django.http import JsonResponse
from email.mime.text import MIMEText
import time

from picktalk.models import *
from myonepick.common import *

# Index 페이지 Query 내용
def index(request):

    nUrl = nowDevice(request)
    user = request.session.get('id', '')

    try :
        cursor = connection.cursor()


        # 메인 베너
        mainbanner = BannerInfo.objects.filter(viewtype='main', nowview='1').order_by("-endtime")[:3]

        # 오디션 추천 ( 순서 상위 4개 표시 )
        if user :
            query = "SELECT AI.num, AI.title, AI.endDate, AI.ordinary, UC.logoImage, (SELECT COUNT(*) FROM audition_pick WHERE userID = '" + user +"' AND auditionNum = AI.num ) AS audiPick, AI.recommend, AI.recommend2,  DATEDIFF(NOW(), endDate) AS diffDate " \
                    "FROM audition_recommend as ar left join audition_info AS AI ON ar.auditionNum = AI.num  " \
                    "LEFT JOIN user_company AS UC ON AI.userID  = UC.userID " \
                    "where (AI.isDelete = '0' or AI.isDelete is null ) and disType = 'main' " \
                    "order by ar.disOrder asc limit 4"
        else :
            query = "SELECT AI.num, AI.title, AI.endDate, AI.ordinary, UC.logoImage, '0' AS audiPick, AI.recommend, AI.recommend2,  DATEDIFF(NOW(), endDate) AS diffDate " \
                    "FROM audition_recommend as ar left join audition_info AS AI ON ar.auditionNum = AI.num  " \
                    "LEFT JOIN user_company AS UC ON AI.userID  = UC.userID " \
                    "where (AI.isDelete = '0' or AI.isDelete is null ) and disType = 'main' " \
                    "order by ar.disOrder asc limit 4"

        result = cursor.execute(query)
        auditions = cursor.fetchall()

        print( auditions )

        # 프로필 Picks Of Onepick
        if user:
            query = "SELECT PI.num, profileImage, ui.name, ui.birth, interCate, interSubCate, mainYoutube, viewCount, cViewCount, pickCount, (SELECT COUNT(*) FROM profile_pick WHERE userID = '" + user + "' AND profileNum = PI.num ) AS proPick, contentType, recommend " \
                    "FROM profile_recommend AS PR LEFT JOIN profile_info AS PI ON PR.profileNum = PI.num " \
                    "     LEFT JOIN user_info AS ui ON PI.userID = ui.userID " \
                    "where PR.disType = 'picks' and ui.name is not null and ui.name != '' and PI.public = '0' and isDelete = '0' " \
                    "ORDER BY RAND() LIMIT 2"
        else:
            query = "SELECT  PI.num, profileImage, ui.name, ui.birth, interCate, interSubCate, mainYoutube, viewCount, cViewCount, pickCount, '0' AS proPick, contentType, recommend " \
                    "FROM profile_recommend AS PR LEFT JOIN profile_info AS PI ON PR.profileNum = PI.num " \
                    "     LEFT JOIN user_info AS ui ON PI.userID = ui.userID " \
                    "where PR.disType = 'picks' and ui.name is not null and ui.name != '' and PI.public = '0' and isDelete = '0'  " \
                    "ORDER BY RAND() LIMIT 2"

        result = cursor.execute(query)
        picksofOnepick = cursor.fetchall()


        # 프로필 기업이 많이 본 리스트
        if user:
            query = "SELECT PI.num, profileImage, ui.name, ui.birth, interCate, interSubCate, mainYoutube, viewCount, cViewCount, pickCount, (SELECT COUNT(*) FROM profile_pick WHERE userID = '" + user + "' AND profileNum = PI.num ) AS proPick, contentType, recommend " \
                    "FROM profile_info AS PI LEFT JOIN user_info AS ui ON PI.userID = ui.userID " \
                    "where ui.name is not null and ui.name != '' and PI.public = '0' " \
                    "ORDER BY cViewCount desc, viewCount desc LIMIT 4"
        else:
            query = "SELECT PI.num, profileImage, ui.name, ui.birth, interCate, interSubCate, mainYoutube, viewCount, cViewCount, pickCount, '0' AS proPick, contentType, recommend " \
                    "FROM profile_info AS PI LEFT JOIN user_info AS ui ON PI.userID = ui.userID " \
                    "where ui.name is not null and ui.name != '' and PI.public = '0'  " \
                    "ORDER BY  cViewCount desc, viewCount desc LIMIT 4"

        result = cursor.execute(query)
        companyManyView = cursor.fetchall()


        # 커뮤니티
        query = "SELECT * FROM ( " \
                "   SELECT num, title, regDate, 'bull' AS tblType FROM `borad_bulletin` UNION ALL " \
                "   SELECT num, title, regDate, 'magazine' AS tblType FROM `borad_magazine` UNION ALL " \
                "   SELECT num, title, regDate, 'notice' AS tblType FROM `qa_notice` where viewType = 'Y'  " \
                ") AS A ORDER BY regDate DESC LIMIT 5"

        result = cursor.execute(query)
        community = cursor.fetchall()

        # 프로필 최신
        if user:
            query = "SELECT p.num, profileImage, ui.name, ui.birth, interCate, interSubCate, mainYoutube, viewCount, cViewCount, pickCount, (SELECT COUNT(*) FROM profile_pick WHERE userID = '" + user + "' AND profileNum = p.num ) AS proPick, contentType, recommend " \
                    "FROM profile_info AS p LEFT JOIN user_info AS ui  ON p.userID = ui.userID " \
                    "WHERE public = '0' and isDelete = '0' and ui.userID != '' and ui.name is not null and ui.name != ''  " \
                    "ORDER BY regDate DESC  " \
                    "LIMIT 6"
        else:
            query = "SELECT p.num, profileImage, ui.name, ui.birth, interCate, interSubCate, mainYoutube, viewCount, cViewCount, pickCount, '0' AS proPick, contentType, recommend " \
                    "FROM profile_info AS p LEFT JOIN user_info AS ui " \
                    "     ON p.userID = ui.userID " \
                    "WHERE public = '0' and isDelete = '0' and ui.userID != '' and ui.name is not null and ui.name != ''  " \
                    "ORDER BY  regDate DESC   " \
                    "LIMIT 6"

        result = cursor.execute(query)
        newProfile = cursor.fetchall()

        # 프로필 추천
        if user:
            query = "SELECT PI.num, profileImage, ui.name, ui.birth, interCate, interSubCate, mainYoutube, viewCount, cViewCount, pickCount, (SELECT COUNT(*) FROM profile_pick WHERE userID = '" + user + "' AND profileNum = PI.num ) AS proPick, contentType, recommend " \
                    "FROM profile_recommend AS PR LEFT JOIN profile_info AS PI ON PR.profileNum = PI.num " \
                    "     LEFT JOIN user_info AS ui ON PI.userID = ui.userID " \
                    "where public = '0' and isDelete = '0' and ui.name is not null and ui.name != '' " \
                    "ORDER BY RAND() LIMIT 6"
        else:
            query = "SELECT PI.num, profileImage, ui.name, ui.birth, interCate, interSubCate, mainYoutube, viewCount, cViewCount, pickCount, '0' AS proPick, contentType, recommend " \
                    "FROM profile_recommend AS PR LEFT JOIN profile_info AS PI ON PR.profileNum = PI.num " \
                    "     LEFT JOIN user_info AS ui ON PI.userID = ui.userID " \
                    "where public = '0' and isDelete = '0' and ui.name is not null and ui.name != '' " \
                    "ORDER BY RAND() LIMIT 6"

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
                query = "SELECT PI.num, profileImage, ui.name, ui.birth, interCate, interSubCate, mainYoutube, viewCount, cViewCount, pickCount, (SELECT COUNT(*) FROM profile_pick WHERE userID = '" + user + "' AND profileNum = PI.num ) AS proPick, contentType, recommend " \
                        "FROM ( SELECT profileNum, COUNT(*) AS views " \
                        "    	FROM profile_view " \
                        "   	WHERE regTime BETWEEN DATE_ADD(NOW(),INTERVAL -1 WEEK ) AND NOW() " \
                        "   	GROUP BY profileNum " \
                        "   	ORDER BY views DESC LIMIT 30 ) A  LEFT JOIN profile_info AS PI ON A.profileNum = PI.num " \
                        "     LEFT JOIN user_info AS ui ON PI.userID = ui.userID " \
                        "where ui.name is not null and ui.name != '' " \
                        "ORDER BY RAND() LIMIT 6"

            else:
                query = "SELECT PI.num, profileImage, ui.name, ui.birth, interCate, interSubCate, mainYoutube, viewCount, cViewCount, pickCount, '0' AS proPick, contentType, recommend " \
                        "FROM ( SELECT profileNum, COUNT(*) AS views " \
                        "    	FROM profile_view " \
                        "   	WHERE regTime BETWEEN DATE_ADD(NOW(),INTERVAL -1 WEEK ) AND NOW() " \
                        "   	GROUP BY profileNum " \
                        "   	ORDER BY views DESC LIMIT 30 ) A  LEFT JOIN profile_info AS PI ON A.profileNum = PI.num " \
                        "     LEFT JOIN user_info AS ui ON PI.userID = ui.userID " \
                        "where ui.name is not null and ui.name != '' " \
                        "ORDER BY RAND() LIMIT 6"


        # 월간 베스트 4,5,6,7,16,17,18,19
        elif nowTimes == 4 or  nowTimes == 5 or  nowTimes == 6 or  nowTimes == 7 or nowTimes == 16 or  nowTimes == 17 or  nowTimes == 18 or nowTimes == 19 :
            if user:
                query = "SELECT PI.num, profileImage, ui.name, ui.birth, interCate, interSubCate, mainYoutube, viewCount, cViewCount, pickCount, (SELECT COUNT(*) FROM profile_pick WHERE userID = '" + user + "' AND profileNum = PI.num ) AS proPick, contentType, recommend " \
                        "FROM ( SELECT profileNum, COUNT(*) AS views " \
                        "    	FROM profile_view " \
                        "   	WHERE regTime BETWEEN DATE_ADD(NOW(),INTERVAL -1 MONTH ) AND NOW() " \
                        "   	GROUP BY profileNum " \
                        "   	ORDER BY views DESC LIMIT 50 ) A  LEFT JOIN profile_info AS PI ON A.profileNum = PI.num " \
                        "     LEFT JOIN user_info AS ui ON PI.userID = ui.userID " \
                        "where ui.name is not null and ui.name != '' " \
                        "ORDER BY RAND() LIMIT 6"

            else:
                query = "SELECT PI.num, profileImage, ui.name, ui.birth, interCate, interSubCate, mainYoutube, viewCount, cViewCount, pickCount, '0' AS proPick, contentType, recommend " \
                        "FROM ( SELECT profileNum, COUNT(*) AS views " \
                        "    	FROM profile_view " \
                        "   	WHERE regTime BETWEEN DATE_ADD(NOW(),INTERVAL -1 MONTH ) AND NOW() " \
                        "   	GROUP BY profileNum " \
                        "   	ORDER BY views DESC LIMIT 50 ) A  LEFT JOIN profile_info AS PI ON A.profileNum = PI.num " \
                        "     LEFT JOIN user_info AS ui ON PI.userID = ui.userID " \
                        "where ui.name is not null and ui.name != '' " \
                        "ORDER BY RAND() LIMIT 6"

        # 전체 베스트 8,9,10,11,20,21,22,23
        elif nowTimes == 8 or nowTimes == 9 or nowTimes == 10 or nowTimes == 11 or nowTimes == 20 or nowTimes == 21 or nowTimes == 22 or nowTimes == 23:
            if user:
                query = "SELECT PI.num, profileImage, ui.name, ui.birth, interCate, interSubCate, mainYoutube, viewCount, cViewCount, pickCount, (SELECT COUNT(*) FROM profile_pick WHERE userID = '" + user + "' AND profileNum = PI.num ) AS proPick, contentType, recommend " \
                        "FROM profile_info AS PI LEFT JOIN user_info AS ui  " \
                        "     ON PI.userID = ui. userID " \
                        "WHERE viewCount > 1000 and ui.name is not null and ui.name != '' " \
                        "ORDER BY RAND() LIMIT 6"
            else:
                query = "SELECT PI.num, profileImage, ui.name, ui.birth, interCate, interSubCate, mainYoutube, viewCount, cViewCount, pickCount, '0' AS proPick, contentType, recommend " \
                        "FROM profile_info AS PI LEFT JOIN user_info AS ui  " \
                        "     ON PI.userID = ui. userID " \
                        "WHERE viewCount > 1000 and ui.name is not null and ui.name != '' " \
                        "ORDER BY RAND() LIMIT 6"


        result = cursor.execute(query)
        bestProfile = cursor.fetchall()

        # 댄스가 특기인 프로필
        if user:
            query = "SELECT p.num, profileImage, ui.name, ui.birth, interCate, interSubCate, mainYoutube, viewCount, cViewCount, pickCount, (SELECT COUNT(*) FROM profile_pick WHERE userID = '" + user + "' AND profileNum = p.num ) AS proPick, contentType " \
                    "FROM profile_info AS p LEFT JOIN user_info AS ui  ON p.userID = ui.userID " \
                    "WHERE public = '0' and isDelete = '0' and ui.userID != '' and ui.name is not null and ui.name != '' and talent like '%댄스%' " \
                    "ORDER BY Rand() DESC  " \
                    "LIMIT 6"
        else:
            query = "SELECT p.num, profileImage, ui.name, ui.birth, interCate, interSubCate, mainYoutube, viewCount, cViewCount, pickCount, '0' AS proPick, contentType " \
                    "FROM profile_info AS p LEFT JOIN user_info AS ui " \
                    "     ON p.userID = ui.userID " \
                    "WHERE public = '0' and isDelete = '0' and ui.userID != '' and ui.name is not null and ui.name != '' and talent like '%댄스%' " \
                    "ORDER BY Rand() DESC   " \
                    "LIMIT 6"

        result = cursor.execute(query)
        danceProfile = cursor.fetchall()


        # 키큰 프로필
        if user:
            query = "SELECT p.num, profileImage, ui.name, ui.birth, interCate, interSubCate, mainYoutube, viewCount, cViewCount, pickCount, (SELECT COUNT(*) FROM profile_pick WHERE userID = '" + user + "' AND profileNum = p.num ) AS proPick, contentType " \
                    "FROM profile_info AS p LEFT JOIN user_info AS ui  ON p.userID = ui.userID " \
                    "WHERE public = '0' and isDelete = '0' and ui.userID != '' and ui.name is not null and ui.name != '' AND ( CASE WHEN gender = 'man' THEN height > 180 END OR CASE WHEN gender = 'girl' THEN height > 168 END  ) " \
                    "ORDER BY Rand() DESC  " \
                    "LIMIT 6"
        else:
            query = "SELECT p.num, profileImage, ui.name, ui.birth, interCate, interSubCate, mainYoutube, viewCount, cViewCount, pickCount, '0' AS proPick, contentType " \
                    "FROM profile_info AS p LEFT JOIN user_info AS ui " \
                    "     ON p.userID = ui.userID " \
                    "WHERE public = '0' and isDelete = '0' and ui.userID != '' and ui.name is not null and ui.name != '' AND ( CASE WHEN gender = 'man' THEN height > 180 END OR CASE WHEN gender = 'girl' THEN height > 168 END  ) " \
                    "ORDER BY Rand() DESC   " \
                    "LIMIT 6"

        result = cursor.execute(query)
        tallProfile = cursor.fetchall()

        # 지역별 프로필
        addrs = ['서울', '인천', '경기', '충청', '대전', '전라', '광주', '강원', '경상', '대구', '울산', '부산', '제주', '서울', '인천', '경기', '충청', '대전', '전라', '광주광역시', '강원', '경상', '대구', '울산', '부산', '제주']
        addr = addrs[nowTimes]
        if user:
            query = "SELECT p.num, profileImage, ui.name, ui.birth, interCate, interSubCate, mainYoutube, viewCount, cViewCount, pickCount, (SELECT COUNT(*) FROM profile_pick WHERE userID = '" + user + "' AND profileNum = p.num ) AS proPick, contentType " \
                    "FROM profile_info AS p LEFT JOIN user_info AS ui  ON p.userID = ui.userID " \
                    "WHERE public = '0' and isDelete = '0' and ui.userID != '' and ui.name is not null and ui.name != '' AND addr1 like '%"+ addr +"%' " \
                    "ORDER BY Rand() DESC  " \
                    "LIMIT 6"
        else:
            query = "SELECT p.num, profileImage, ui.name, ui.birth, interCate, interSubCate, mainYoutube, viewCount, cViewCount, pickCount, '0' AS proPick, contentType " \
                    "FROM profile_info AS p LEFT JOIN user_info AS ui " \
                    "     ON p.userID = ui.userID " \
                    "WHERE public = '0' and isDelete = '0' and ui.userID != '' and ui.name is not null and ui.name != '' AND addr1 like '%"+ addr +"%' " \
                    "ORDER BY Rand() DESC   " \
                    "LIMIT 6"

        result = cursor.execute(query)
        addrProfile = cursor.fetchall()


        connection.commit()
        connection.close()

        popupList = PopupInfo.objects.all()

    except :
        print("error!")
        connection.rollback()

    return render(request, nUrl + '/index.html',
                  {'auditions': auditions, 'newProfile': newProfile , 'recomProfile' : recomProfile,
                   'bestProfile' : bestProfile, 'mainbanner' : mainbanner, "popupList" : popupList,
                   'picksofOnepick': picksofOnepick, 'companyManyView' : companyManyView, 'community' : community,
                   'danceProfile':danceProfile, "tallProfile" : tallProfile, "addr" : addr, "addrProfile" : addrProfile  })



def advertise(request) :

    nUrl = nowDevice(request)

    return render(request, nUrl + '/advertise.html')



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


def proList(request, type, page, num, filter) :

    nUrl = nowDevice(request)

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

    return render(request,  nUrl + 'user/proList.html',
                  {"type": type, "profile": profile, "filter" : filter, "paging":paging, "page": page,
                   "leftPage": page - 1, "rightPage": page + 1, "lastPage": allPage,
                   "allCount" : cursor.rowcount, "allList" : len(allList), "num": num })

def proList2(request, type, page, num, filter) :

    nUrl = nowDevice(request)

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

    return render(request,  nUrl + 'user/ajax_proList.html', {"type": type, "page":page, "profile": profile,"num": num })



def applyList(request, num) :

    nUrl = nowDevice(request)

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
            where = where + " and isCareer = '0' and ( careerYear < '1' or careerYear is null ) "
        else:
            where = where + " and isCareer = '0' and careerYear >= " + str(careerRadio) + " "
    elif career1 != "" and career2 != "":
        where = where + " and isCareer = '0' and careerYear >= '" + str(career1) + "' and careerYear <= '" + str(career2) + "'"
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

    print(query)
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

    return render(request, nUrl + '/user/proList_apply.html',
                  {"profile": profile, "filter" : filter, "paging":paging, "page": page,
                   "leftPage": page - 1, "rightPage": page + 1, "lastPage": allPage,"allCount" : cursor.rowcount, "allList" : len(allList), "num": num,
                   "nationality":nationality, "geneder": geneder, "military": military, "ageRadio": ageRadio
                  , "age1": age1, "age2": age2, "school": school, "heightRadio": heightRadio, "height1": height1, "height2": height2
                  , "careerRadio": careerRadio, "career1": career1, "career2": career2, "foreSpec": foreSpec, "findSpec": findSpec, "tagSpec": tagSpec,
                  "foreList": foreign, "spList": specList, "tagSpecList": tagSpecList, "speList": specialty, "tagList": tagList })



def gsdv(request) :

    nUrl = nowDevice(request)

    return render(request,  nUrl + '/gsdv.txt')



def downstime(request) :

    return render(request, 'picktalk/downstime.html')
