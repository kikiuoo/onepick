from django.db.models import Subquery
from django.shortcuts import render
from django.http import HttpResponse
from django.template import  loader
from django.db import connection
from audition.models import Audition
from profiles.models import Profile

# Create your views here.

# Index 페이지 Query 내용
def index(request):
    try:
        cursor = connection.cursor()

        # 메인 베너

        auditions = Audition.objects.all().order_by('-regTime').distinct()[:4] # 오디션 최근 Update 순으로 4개 확인.
        profiles = Profile.objects.all().order_by('-regTime').distinct()[:4] # 프로필

        # 소베너 - 코드 변경 필요.
        strSql = "select image, url from banner_pickchoice where isDeleted = 0 order by banner_pickchoice.index asc limit 2 "

        result = cursor.execute(strSql)
        datas = cursor.fetchall()

        pickChoises = []
        for data in datas :
            row = {
                'url' : data[1],
                'image' : data[0]
            }
            pickChoises.append(row)

        # 알바픽 정보


        connection.commit()
        connection.close()

    except:
        connection.rollback()
        print('Faild DB Connection')

    return render(request, 'picktalk/index.html',
                  {'auditions': auditions, 'profiles': profiles, 'pickChoises': pickChoises})
