import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template import  loader
from django.db import connection

from picktalk.models import *
from django.db.models import Q
from django.utils import timezone

from myonepick.common import *

urlBase = "onepickAdmin/display/"

def audiList(request):

    audiType = request.GET.get('audiType', "main")

    try:
        cursor = connection.cursor()

        query = "SELECT ai.num, disOrder, companyName, title, ai.regTime, ar.num " \
                "FROM audition_recommend AS ar LEFT JOIN audition_info AS ai " \
                "     ON ar.auditionNum = ai.num " \
                "     LEFT JOIN user_company AS uc ON ai.userID = uc.userID " \
                "WHERE disType = '"+audiType+"' and isDelete = '0'  " \
                "order by disOrder asc"

        result = cursor.execute(query)
        recommend = cursor.fetchall()

        query = "SELECT ai.num, companyName, title, ai.regTime, " \
                "       ( SELECT COUNT(*) FROM audition_recommend WHERE auditionNum = ai.num and disType = '" + audiType + "' ) AS recomm " \
                "FROM audition_info AS ai LEFT JOIN user_company AS uc " \
                "     ON ai.userID = uc.userID " \
                "WHERE  isDelete = '0' " \
                "ORDER BY ai.regTime DESC"

        result = cursor.execute(query)
        audition = cursor.fetchall()

        connection.commit()
        connection.close()

    except:
        connection.rollback()

    return render( request, urlBase + "audiList.html",
                   {'pageType': "display", "recommend" : recommend, "type" : audiType, "audition": audition})


def findAudition(request) :

    word = request.GET.get("word", "")
    type = request.GET.get("type", "")

    cursor = connection.cursor()

    query = "SELECT ai.num, companyName, title, ai.regTime, " \
            "       ( SELECT COUNT(*) FROM audition_recommend WHERE auditionNum = ai.num and disType = '"+type+"' ) AS recomm " \
            "FROM audition_info AS ai LEFT JOIN user_company AS uc " \
            "     ON ai.userID = uc.userID " \
            "WHERE  isDelete = '0' and ( title LIKE '%"+word+"%' OR ai.num = '"+word+"' OR uc.companyName LIKE '%"+word+"%' ) " \
            "ORDER BY ai.regTime DESC"

    result = cursor.execute(query)
    recommend = cursor.fetchall()

    connection.commit()
    connection.close()


    return render( request, urlBase + "ajax_audiList.html", {'pageType': "display", "recommend" : recommend})


def saveRecommend(request) :

    audition = request.GET.get("audition", "")
    type = request.GET.get("type", "")

    AuditionRecommend.objects.filter(distype=type).delete() # 기존 데이터 삭제.

    audiList = audition.split(',')

    disCount = 1;
    for audi in audiList :
        AuditionRecommend.objects.create(distype=type, auditionnum=audi, disorder=disCount)
        disCount = disCount + 1

    return JsonResponse({"code": "0"})


def updateOrder(request) :

    cType = request.GET.get("cType", "")
    type = request.GET.get("type", "")
    active = request.GET.get("active", "")
    order = request.GET.get("order", "")


    if cType == "allDown" :
        updateCount = AuditionRecommend.objects.filter(distype=type)
        updateList = AuditionRecommend.objects.filter(distype=type, disorder__gte=order)

        for update in updateList :
            if str(update.num) == str(active) :
                update.disorder = updateCount.count()
            else :
                update.disorder = update.disorder - 1
            update.save()

    elif cType == "allUp" :
        updateList = AuditionRecommend.objects.filter(distype=type, disorder__lte=order)

        for update in updateList :
            if str(update.num) == str(active) :
                update.disorder = 1
            else :
                update.disorder = update.disorder + 1
            update.save()


    elif cType == "down" :
        updateList = AuditionRecommend.objects.get(distype=type, disorder=order)
        updateList2 = AuditionRecommend.objects.get(distype=type, disorder=int(order)+1)
        updateList.disorder = int(order) + 1
        updateList.save()

        updateList2.disorder = int(order)
        updateList2.save()

    elif cType == "up" :
        updateList = AuditionRecommend.objects.get(distype=type, disorder=order)
        updateList2 = AuditionRecommend.objects.get(distype=type, disorder=int(order)-1)
        updateList.disorder = int(order) - 1
        updateList.save()

        updateList2.disorder = int(order)
        updateList2.save()

    return JsonResponse({"code": "0"})
