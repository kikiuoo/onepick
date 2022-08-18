import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template import  loader
from django.db import connection

from picktalk.models import *
from django.db.models import Q
from django.utils import timezone

from myonepick.common import *

urlBase = "onepickAdmin/notice/"

def list(request, type, page):

    block = 10
    start = (page - 1) * block
    end = page * block

    if type == "all" :
        noticeList = QaNotice.objects.all().order_by("-regdate")
    elif type == "view" :
        noticeList = QaNotice.objects.filter(viewtype="Y").order_by("-regdate")
    else :
        noticeList = QaNotice.objects.filter(viewtype="N").order_by("-regdate")

    notice = noticeList[start:end]
    allPage = (len(noticeList) / block) + 1
    paging = getPageList_v2(page, allPage)

    return render( request, urlBase + "list.html", {'pageType': "notice", "noticeList":notice, "paging":paging, "page" : page,
                                                    "leftPage" : page-1, "rightPage" : page+1, "lastPage" : allPage, "type":type })


def write(request):

    return render( request, urlBase + "write.html", {'pageType': "notice" })

def writeCallBack(request):
    title = request.POST['title']
    content = request.POST['content']
    view = request.POST['view']

    user = request.session.get('adminID', '')
    nowTime = timezone.now()
    noticeSave = QaNotice.objects.create(userid=user, title=title, content=content, regdate=nowTime, contenttype='old',
                                         viewtype=view, viewcount=0)

    return JsonResponse({"code": "0"})

def summerImageUpload(request) :
    file = request.FILES.getlist("file", "")
    for image in file:
        sub = image.name.split('.')[-1]
        url = uploadFile(image, "photos/notice/", sub)  # 파일 업로드
        logoImage = url

    return JsonResponse({"code": "0", "url" :  logoImage})


def viewer(request, num):
    notice = QaNotice.objects.get(num=num)
    return render( request, urlBase + "viewer.html", {'pageType': "notice", "notice" : notice })


def edit(request, num):
    notice = QaNotice.objects.get(num=num)
    return render( request, urlBase + "edit.html", {'pageType': "notice", "notice" : notice })

def editCallBack(request):
    num = request.POST['num']
    title = request.POST['title']
    content = request.POST['content']
    view = request.POST['view']

    notice = QaNotice.objects.get(num=num)
    notice.title = title
    notice.content = content
    notice.viewtype = view
    notice.save()

    return JsonResponse({"code": "0"})



def delete(request, num):
    notice = QaNotice.objects.get(num=num)
    notice.delete()
    return redirect('/onepickAdmin/notice/list/all/1/')