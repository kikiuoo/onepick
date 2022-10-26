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
    user = request.session.get('adminID', '')
    if user == "" or user == None:
        message = '로그인 후 이용가능합니다..'
        return HttpResponse("<script>alert('" + message + "'); window.location.href = '/onepickAdmin'; </script>")

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

    num = request.GET.get("num", "")
    rType = request.GET.get("rType", "")
    type = request.GET.get("type", "")

    if rType == "add" :
        # 추천 목록에 추가.
        audiRecom = AuditionRecommend.objects.filter(distype=type)
        AuditionRecommend.objects.create(distype=type, auditionnum=num, disorder=(audiRecom.count()+1))

    elif rType == "delete" :
        audiRecom = AuditionRecommend.objects.get(auditionnum=num, distype=type)
        print(audiRecom)

        updateList = AuditionRecommend.objects.filter(distype=type, disorder__gte=audiRecom.disorder)

        for update in updateList:
            update.disorder = update.disorder - 1
            update.save()

        audiRecom.delete()

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







# 프로필 진열관리
def proList(request):
    user = request.session.get('adminID', '')
    if user == "" or user == None:
        message = '로그인 후 이용가능합니다..'
        return HttpResponse("<script>alert('" + message + "'); window.location.href = '/onepickAdmin'; </script>")

    viewType = request.GET.get('viewType', "main")

    try:
        cursor = connection.cursor()

        query = "SELECT PI.num, ui.name, ui.birth, PI.interCate, PI.interSubCate, PI.profileImage, PR.num, PR.disOrder, contentType " \
                "FROM profile_recommend AS PR LEFT JOIN profile_info AS PI  ON PR.profileNum = PI.num " \
                "     left join user_info as ui on PI.userID = ui.userID  " \
                "WHERE disType = '"+viewType+"'  " \
                "order by disOrder asc"

        result = cursor.execute(query)
        recommend = cursor.fetchall()

        query = "SELECT PI.num, ui.name, ui.birth, PI.interCate, PI.interSubCate, PI.profileImage, " \
                " ( SELECT COUNT(*) FROM profile_recommend WHERE profileNum = PI.num AND disType = 'main' ) AS recomm, contentType  " \
                "FROM profile_info AS PI LEFT JOIN user_info AS ui " \
                "     ON PI.userID = ui.userID " \
                "WHERE public = '0' ORDER BY `upDate` DESC,RegDate DESC LIMIT 50"

        result = cursor.execute(query)
        profile = cursor.fetchall()

        connection.commit()
        connection.close()

    except:
        connection.rollback()

    return render( request, urlBase + "proList.html",
                   {'pageType': "display", "recommend" : recommend, "type" : viewType, "profile": profile})



def findProfile(request) :

    word = request.GET.get("word", "")
    type = request.GET.get("type", "")

    cursor = connection.cursor()

    query = "SELECT PI.num, ui.name, ui.birth, PI.interCate, PI.interSubCate, PI.profileImage, " \
            " ( SELECT COUNT(*) FROM profile_recommend WHERE profileNum = PI.num AND disType = 'main' ) AS recomm, contentType  " \
            "FROM profile_info AS PI LEFT JOIN user_info AS ui " \
            "     ON PI.userID = ui.userID " \
            "WHERE public = '0'  and ( name LIKE '%"+word+"%' OR PI.num = '"+word+"' OR ui.birth LIKE '%"+word+"%' ) " \
            " ORDER BY `upDate` DESC,RegDate DESC LIMIT 50"

    result = cursor.execute(query)
    profile = cursor.fetchall()

    connection.commit()
    connection.close()


    return render( request, urlBase + "ajax_proList.html", {'pageType': "display", "profile" : profile})


def proSaveRecommend(request) :

    num = request.GET.get("num", "")
    rType = request.GET.get("rType", "")
    type = request.GET.get("type", "")

    if rType == "add" :
        print("add")
        # 추천 목록에 추가.
        proRecom = ProfileRecommend.objects.filter(distype=type)
        ProfileRecommend.objects.create(distype=type, profilenum=num, disorder=(proRecom.count()+1))

    elif rType == "delete" :
        proRecom = ProfileRecommend.objects.get(distype=type, profilenum=num)

        updateList = ProfileRecommend.objects.filter(distype=type, disorder__gte=proRecom.disorder)

        for update in updateList:
            update.disorder = update.disorder - 1
            update.save()

        proRecom.delete()

    return JsonResponse({"code": "0"})


# 배너 진열관리
def bannerList(request):
    user = request.session.get('adminID', '')
    if user == "" or user == None:
        message = '로그인 후 이용가능합니다..'
        return HttpResponse("<script>alert('" + message + "'); window.location.href = '/onepickAdmin'; </script>")

    viewType = request.GET.get('viewType', "all")
    page = request.GET.get('page', "1")

    page = int(page)

    block = 10
    start = (page - 1) * block
    end = page * block

    if viewType == "all" :
        bannerList = BannerInfo.objects.all().order_by("-num")
    else :
        bannerList = BannerInfo.objects.filter(viewtype=viewType).order_by("-num")

    banner = bannerList[start:end]
    allPage = int(len(bannerList) / block) + 1
    paging = getPageList_v2(page, allPage)

    return render( request, urlBase + "bannerList.html",
                   {'pageType': "display", "bannerList": banner, "paging": paging, "page": page,
                    "leftPage": page - 1, "rightPage": page + 1, "lastPage": allPage, "type": viewType})


def bannerWrite(request):
    user = request.session.get('adminID', '')
    if user == "" or user == None:
        message = '로그인 후 이용가능합니다..'
        return HttpResponse("<script>alert('" + message + "'); window.location.href = '/onepickAdmin'; </script>")

    return render( request, urlBase + "bannerWrite.html", {'pageType': "display"})


def writeCallback(request):

    title = request.POST['title']
    viewType = request.POST['viewType']
    link = request.POST['url']
    userImage = request.FILES.getlist('userImage[]')
    startDate = request.POST['startDate']
    endDate = request.POST['endDate']

    nowTime = timezone.now()

    image_banner = ""
    count = 0
    for image in userImage:
        count = count + 1
        sub = image.name.split('.')[-1]
        url = uploadFile(image, "photos/profiles/banner/", sub)

        image_banner = url


    saveBanner = BannerInfo.objects.create(title=title, viewtype=viewType, url=link, image=image_banner,
                                           nowview='1', viewcount=0, clickcount=0,
                                           starttime=startDate + " 00:00:00", endtime=endDate + " 23:59:59",
                                           regtime=nowTime)

    return redirect('/onepickAdmin/display/banner/')


def bannerEdit(request, num):
    user = request.session.get('adminID', '')
    if user == "" or user == None:
        message = '로그인 후 이용가능합니다..'
        return HttpResponse("<script>alert('" + message + "'); window.location.href = '/onepickAdmin'; </script>")

    banner = BannerInfo.objects.get(num=num)

    return render( request, urlBase + "bannerEdit.html", {'pageType': "display", "banner": banner})


def editCallback(request):

    num  = request.POST['num']
    title = request.POST['title']
    viewType = request.POST['viewType']
    link = request.POST['url']
    userImage = request.FILES.getlist('userImage[]')
    startDate = request.POST['startDate']
    endDate = request.POST['endDate']

    nowTime = timezone.now()

    banner = BannerInfo.objects.get(num=num)

    image_banner = banner.image
    if userImage != "" :
        # 기존 이미지 삭제
        for rmImages in userImage:
            if (rmImages == ""): continue
            deleteFile(rmImages)

        count = 0
        for image in userImage:
            count = count + 1
            sub = image.name.split('.')[-1]
            url = uploadFile(image, "photos/profiles/banner/", sub)

            image_banner = url

    banner.title = title
    banner.viewtype = viewType
    banner.url = link
    banner.image = image_banner
    banner.starttime = startDate
    banner.endtime = endDate

    banner.save()

    return redirect('/onepickAdmin/display/banner/')


def bannerDelete(request, num):

    banner = BannerInfo.objects.get(num=num)
    banner.delete()

    return redirect('/onepickAdmin/display/banner/')

