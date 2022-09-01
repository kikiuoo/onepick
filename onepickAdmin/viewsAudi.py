import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template import  loader
from django.db import connection

from picktalk.models import *
from django.db.models import Q
from django.utils import timezone

from myonepick.common import *

urlBase = "onepickAdmin/audi/"

def list(request, type,  page):

    try:
        cursor = connection.cursor()

        block = 10
        start = (page - 1) * block
        end = page * block

        if type == "all" :
            where = " "
        elif type == "ing":
            where = " AND endDate >= NOW() "
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

    try:
        cursor = connection.cursor()

        block = 10
        start = (page - 1) * block
        end = page * block

        if type == "all" :
            where = " "
        elif type == "ing":
            where = " AND endDate >= NOW() "
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


    return render( request, urlBase + "listSearch.html", {'pageType': "audi", "auditionList":audition, "paging":paging, "page" : page,
                                                    "leftPage" : page-1, "rightPage" : page+1, "lastPage" : allPage, "cateList" : cateList,
                                                    "type": type, "word":word})

