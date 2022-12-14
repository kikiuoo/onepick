from django.http import JsonResponse
from django.utils import timezone

from picktalk.models import *
from myonepick.common import *

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
