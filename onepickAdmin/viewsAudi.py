import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.db import connection

from picktalk.models import *
from django.db.models import Q
from django.utils import timezone

from myonepick.common import *

urlBase = "onepickAdmin/audi/"

def list(request, type,  page):
    user = request.session.get('adminID', '')
    if user == "" or user == None:
        message = '로그인 후 이용가능합니다..'
        return HttpResponse("<script>alert('" + message + "'); window.location.href = '/onepickAdmin'; </script>")

    try:
        cursor = connection.cursor()

        block = 10
        start = (page - 1) * block
        end = page * block

        if type == "all" :
            where = " "
        elif type == "ing":
            where = " AND ( endDate >= NOW() or ordinary = '1' ) "
        else :
            where = " AND endDate < NOW() "

        query = "SELECT ai.num, uc.companyName, ai.title, ai.regTime, ai.startDate, ai.endDate, ai.viewCount, " \
                "	(SELECT COUNT(*) FROM audition_apply WHERE auditionNum = ai.num) AS applyCount " \
                "FROM audition_info AS ai LEFT JOIN user_company AS uc ON ai.userID = uc.userID " \
                "WHERE isDelete = '0' " + where + "  " \
                "ORDER BY ai.regTime DESC"

        result = cursor.execute(query)
        auditionAll = cursor.fetchall()

        query = "SELECT ai.num, uc.companyName, ai.title, ai.regTime, ai.startDate, ai.endDate, ai.viewCount, " \
                "	(SELECT COUNT(*) FROM audition_apply WHERE auditionNum = ai.num) AS applyCount " \
                "FROM audition_info AS ai LEFT JOIN user_company AS uc ON ai.userID = uc.userID " \
                "WHERE isDelete = '0' " + where + " " \
                "ORDER BY ai.regTime DESC LIMIT " + str(start) + ", " + str(block)

        result = cursor.execute(query)
        audition = cursor.fetchall()

        allPage = int(len(auditionAll) / block) + 1
        paging = getPageList_v2(page, allPage)

        connection.commit()
        connection.close()

        cateList = CateMain.objects.all().order_by("cateorder")

    except:
        connection.rollback()


    return render( request, urlBase + "list.html", {'pageType': "audi", "auditionList":audition, "paging":paging, "page" : page,
                                                    "leftPage" : page-1, "rightPage" : page+1, "lastPage" : allPage, "cateList" : cateList,
                                                    "type": type})


def listSearch(request, type, word, page):

    user = request.session.get('adminID', '')
    if user == "" or user == None :
        message = '로그인 후 이용가능합니다..'
        return HttpResponse("<script>alert('" + message + "'); window.location.href = '/onepickAdmin'; </script>")

    try:
        cursor = connection.cursor()

        block = 10
        start = (page - 1) * block
        end = page * block

        if type == "all" :
            where = " "
        elif type == "ing":
            where = " AND ( endDate >= NOW() or ordinary = '1' ) "
        else :
            where = " AND endDate < NOW() "

        query = "SELECT ai.num, uc.companyName, ai.title, ai.regTime, ai.startDate, ai.endDate, ai.viewCount, " \
                "	(SELECT COUNT(*) FROM audition_apply WHERE auditionNum = ai.num) AS applyCount " \
                "FROM audition_info AS ai LEFT JOIN user_company AS uc ON ai.userID = uc.userID " \
                "WHERE isDelete = '0' " + where + " and ( uc.companyName like '%"+word+"%' or ai.title like '%"+word+"%' ) " \
                "ORDER BY ai.regTime DESC"

        result = cursor.execute(query)
        audiAll = cursor.fetchall()

        query = "SELECT ai.num, uc.companyName, ai.title, ai.regTime, ai.startDate, ai.endDate, ai.viewCount, " \
                "	(SELECT COUNT(*) FROM audition_apply WHERE auditionNum = ai.num) AS applyCount " \
                "FROM audition_info AS ai LEFT JOIN user_company AS uc ON ai.userID = uc.userID " \
                "WHERE isDelete = '0' " + where + "  and ( uc.companyName like '%"+word+"%' or ai.title like '%"+word+"%' ) " \
                "ORDER BY ai.regTime DESC LIMIT " + str(start) + ", " + str(block)

        result = cursor.execute(query)
        audition = cursor.fetchall()

        allPage = int(len(audiAll) / block) + 1
        paging = getPageList_v2(page, allPage)

        connection.commit()
        connection.close()

        cateList = CateMain.objects.all().order_by("cateorder")

    except:
        connection.rollback()

    return render(request, urlBase + "listSearch.html",
                  {'pageType': "audi", "auditionList": audition, "paging": paging, "page": page,
                   "leftPage": page - 1, "rightPage": page + 1, "lastPage": allPage, "cateList": cateList,
                   "type": type, "word": word})

## saveRecommendAudi 추가
def saveRecommendAudi(request):
    num = request.GET.get("num", "")
    rType = request.GET.get("rType", "")
    type = request.GET.get("type", "")
    checkedImage = request.GET.get("checkedImage", "")

    if rType == "add":
        auditionInfo = AuditionInfo.objects.get(num=num)

        if checkedImage == "recommendAudiImageEmpty":
            auditionInfo.recommend = "1"
            auditionInfo.recommend2 = "0"
            auditionInfo.save()

        elif checkedImage == "recommendAudiImageFull":
            auditionInfo.recommend = "0"
            auditionInfo.recommend2 = "1"
            auditionInfo.save()

        # 추천 목록에 현재 오디션 num이 있다면 distype, disorder update.
        try:
            exists_status = AuditionRecommend.objects.get(auditionnum=num)
            exists_status.distype = checkedImage
            audiRecom = AuditionRecommend.objects.filter(distype=checkedImage)

            exists_status.disorder = (audiRecom.count() + 1)
            exists_status.save()

            return JsonResponse({"code": "update"})

        # 추천 목록에 현재 오디션 num이 없다면 distype, disorder add
        except AuditionRecommend.DoesNotExist:
            exists_status = None

            audiRecom = AuditionRecommend.objects.filter(distype=checkedImage)
            AuditionRecommend.objects.create(distype=checkedImage, auditionnum=num, disorder=(audiRecom.count() + 1))

            print("ghgh", exists_status)
            return JsonResponse({"code": "add"})

    elif rType == "delete":
        # 추천 목록에 삭제

        auditionInfo = AuditionInfo.objects.get(num=num)
        auditionInfo.recommend = "0"
        auditionInfo.recommend2 = "0"
        auditionInfo.save()

        audiRecom = AuditionRecommend.objects.get(distype=checkedImage, auditionnum=num)
        print("audiRecom", audiRecom)
        print("audiRecom", audiRecom.disorder)

        updateList = AuditionRecommend.objects.filter(distype=checkedImage, disorder__gte=audiRecom.disorder)
        print("updateList", updateList)

        for update in updateList:
            update.disorder = update.disorder - 1
            update.save()

        AuditionRecommend.objects.filter(auditionnum=num).delete()
        return JsonResponse({"code": "delete"})

    return JsonResponse({"code": "0000"})
