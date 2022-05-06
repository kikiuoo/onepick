from django.db.models import Subquery
from django.shortcuts import render
from django.http import HttpResponse
from django.template import  loader
from django.db import connection

from picktalk.models import *

# Create your views here.

# Index 페이지 Query 내용
def index(request):
    # 메인 베너
    mainbanner = EventBanner.objects.filter(position="main")

    auditions = AuditionInfo.objects.all().order_by('-regtime').distinct()[:4] # 오디션 최근 Update 순으로 4개 확인.
    profiles = ProfileInfo.objects.all().order_by('-regdate').distinct()[:4] # 프로필

    # 소베너 - 코드 변경 필요.
    subBanner = EventBanner.objects.filter(position="mainSub")


    return render(request, 'picktalk/index.html',
                  {'auditions': auditions, 'profiles': profiles , 'mainbanner' : mainbanner, 'subBanner' : subBanner })

