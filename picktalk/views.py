from django.db.models import Subquery
from django.shortcuts import render
from django.http import HttpResponse
from django.template import  loader
from django.db import connection
from django.utils import timezone
from django.http import JsonResponse

from picktalk.models import *

# Create your views here.

# Index 페이지 Query 내용
def index(request):

    try :
        cursor = connection.cursor()

        # 메인 베너
        mainbanner = EventBanner.objects.filter(position="main")

        query = "SELECT AI.num, AI.title, AI.endDate, AI.ordinary, UC.logoImage, (SELECT COUNT(*) FROM audition_pick WHERE userID = 'kakao_2207974285' AND auditionNum = AI.num ) AS audiPick" \
                " FROM audition_info AS AI LEFT JOIN user_company AS UC ON AI.userID  = UC.userID " \
                "order by AI.regTime desc LIMIT 8 "
        result = cursor.execute(query)
        auditions = cursor.fetchall()

        profiles = ProfileInfo.objects.all().order_by('-regdate').distinct()[:4] # 프로필

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
            pick = ProfilePick.objects.create( profilenum=num, userid=userID, regtime=nowTime )

    else : # on : 삭제

        if tableName == "audition" :
            pick = AuditionPick.objects.filter( auditionnum=num, userid=userID )
        else :
            pick = ProfilePick.objects.filter( profilenum=num, userid=userID )

        pick.delete()

    return JsonResponse({"code": "0"})
