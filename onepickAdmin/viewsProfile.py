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

def list(request, page):

    block = 10
    start = (page - 1) * block
    end = page * block

    userList = UserInfo.objects.filter(usertype__contains="COMPANY", phone__isnull=False).order_by("-regtime")

    user = userList[start:end]
    allPage = (len(userList) / block) + 1
    paging = getPageList_v2(page, allPage)

    return render( request, urlBase + "list.html", {'pageType': "profile", "userList":user, "paging":paging, "page" : page,
                                                    "leftPage" : page-1, "rightPage" : page+1, "lastPage" : allPage })

