import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template import  loader
from django.db import connection

from picktalk.models import *
from django.db.models import Q
from django.utils import timezone

from myonepick.common import *

urlBase = "onepickAdmin/profile/"

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
        else :
            where = " and interCate = '"+type+"' "

        query = "SELECT pi.num, cm.cateName, cs.cateName, ui.name, ui.birth, ui.phone, ui.gender, pi.public, pi.regDate " \
                "FROM profile_info AS pi LEFT JOIN user_info ui ON pi.userID = ui.userID " \
                "     LEFT JOIN cate_main cm ON pi.interCate = cm.cateCode " \
                "     LEFT JOIN cate_sub cs ON pi.interSubCate = cs.subCate " \
                "WHERE isDelete = '0' "+ where +" ORDER BY regDate DESC"

        result = cursor.execute(query)
        profileAll = cursor.fetchall()

        query = "SELECT pi.num, cm.cateName, cs.cateName, ui.name, ui.birth, ui.phone, ui.gender, pi.public, pi.regDate " \
                "FROM profile_info AS pi LEFT JOIN user_info ui ON pi.userID = ui.userID " \
                "     LEFT JOIN cate_main cm ON pi.interCate = cm.cateCode " \
                "     LEFT JOIN cate_sub cs ON pi.interSubCate = cs.subCate " \
                "WHERE isDelete = '0' "+ where +" ORDER BY regDate DESC LIMIT " + str(start) + ", " + str(block)

        result = cursor.execute(query)
        profile = cursor.fetchall()

        allPage = int(len(profileAll) / block) + 1
        paging = getPageList_v2(page, allPage)

        connection.commit()
        connection.close()

        cateList = CateMain.objects.all().order_by("cateorder")

    except:
        connection.rollback()


    return render( request, urlBase + "list.html", {'pageType': "profile", "profileList":profile, "paging":paging, "page" : page,
                                                    "leftPage" : page-1, "rightPage" : page+1, "lastPage" : allPage, "cateList" : cateList,
                                                    "type": type})

def listSearch(request, type, word, page):
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
        else :
            where = " and interCate = '"+type+"' "

        query = "SELECT pi.num, cm.cateName, cs.cateName, ui.name, ui.birth, ui.phone, ui.gender, pi.public, pi.regDate " \
                "FROM profile_info AS pi LEFT JOIN user_info ui ON pi.userID = ui.userID " \
                "     LEFT JOIN cate_main cm ON pi.interCate = cm.cateCode " \
                "     LEFT JOIN cate_sub cs ON pi.interSubCate = cs.subCate " \
                "WHERE isDelete = '0' "+ where +" and ( ui.name like '%"+word+"%' or  ui.phone like '%"+word+"%' ) ORDER BY regDate DESC"

        result = cursor.execute(query)
        profileAll = cursor.fetchall()

        query = "SELECT pi.num, cm.cateName, cs.cateName, ui.name, ui.birth, ui.phone, ui.gender, pi.public, pi.regDate " \
                "FROM profile_info AS pi LEFT JOIN user_info ui ON pi.userID = ui.userID " \
                "     LEFT JOIN cate_main cm ON pi.interCate = cm.cateCode " \
                "     LEFT JOIN cate_sub cs ON pi.interSubCate = cs.subCate " \
                "WHERE isDelete = '0' "+ where +" and ( ui.name like '%"+word+"%' or  ui.phone like '%"+word+"%' ) ORDER BY regDate DESC LIMIT " + str(start) + ", " + str(block)

        result = cursor.execute(query)
        profile = cursor.fetchall()

        allPage = int(len(profileAll) / block) + 1
        paging = getPageList_v2(page, allPage)

        connection.commit()
        connection.close()

        cateList = CateMain.objects.all().order_by("cateorder")

    except:
        connection.rollback()


    return render( request, urlBase + "listSearch.html", {'pageType': "profile", "profileList":profile, "paging":paging, "page" : page,
                                                    "leftPage" : page-1, "rightPage" : page+1, "lastPage" : allPage, "cateList" : cateList,
                                                    "type": type, "word":word})

