import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import  loader
from django.db import connection

from picktalk.models import *
import boto3
from django.conf import settings
from django.utils import timezone
import hashlib


def md5_generator(str):
    m = hashlib.md5()
    m.update(str.encode())
    return m.hexdigest()


# 오디션 /audi ...
#  -- 오디션 메인
#     /audi/main/actor/ : 배우 탭 활성화, 기본 탭.
#     /audi/main/model/ : 모델 탭 활성화
#     /audi/main/singer/ : 가수 탭 활성화
def audi_index(request, cate_type): # 오디션 Main
    try:
        cursor = connection.cursor()

        # 메인 베너
        subBanner = EventBanner.objects.filter(position="audi", nowview="1")

        user = request.session.get('id', '')

        if user:
            query = "SELECT AI.num, AI.title, AI.endDate, AI.ordinary, UC.logoImage, (SELECT COUNT(*) FROM audition_pick WHERE userID = '" + user + "' AND auditionNum = AI.num ) AS audiPick" \
                    " FROM audition_info AS AI LEFT JOIN user_company AS UC ON AI.userID  = UC.userID " \
                    "WHERE recommend = '1' " \
                    "order by AI.recOrder ASC LIMIT 4 "
        else:
            query = "SELECT AI.num, AI.title, AI.endDate, AI.ordinary, UC.logoImage, '0' AS audiPick" \
                    " FROM audition_info AS AI LEFT JOIN user_company AS UC ON AI.userID  = UC.userID " \
                    "WHERE recommend = '1' " \
                    "order by AI.recOrder ASC LIMIT 4 "

        result = cursor.execute(query)
        recomAudi = cursor.fetchall()

        if user:
            query = "SELECT AI.num, AI.title, AI.endDate, AI.ordinary, UC.logoImage, (SELECT COUNT(*) FROM audition_pick WHERE userID = '" + user + "' AND auditionNum = AI.num ) AS audiPick" \
                    " FROM audition_info AS AI LEFT JOIN user_company AS UC ON AI.userID  = UC.userID " \
                    "WHERE ordinary = '0' AND endDate >= NOW()" \
                    "order by AI.endDate ASC LIMIT 4 "
        else:
            query = "SELECT AI.num, AI.title, AI.endDate, AI.ordinary, UC.logoImage, '0' AS audiPick " \
                    "FROM audition_info AS AI LEFT JOIN user_company AS UC ON AI.userID  = UC.userID " \
                    "WHERE ordinary = '0' AND endDate >= NOW()" \
                    "order by AI.endDate ASC LIMIT 4 "

        result = cursor.execute(query)
        finishAudi = cursor.fetchall()

        query = "SELECT ai.num, ai.title, cm.cateName, ai.career, ai.age, ai.endDate, ai.regTime, ai.ordinary, uc.companyName, DATEDIFF(NOW(),  ai.regTime) AS diffDate " \
                "FROM audition_info AS ai LEFT JOIN cate_main AS cm ON ai.cate = cm.cateCode " \
                "    LEFT JOIN  user_company AS uc ON ai.userID = uc.userID " \
                "ORDER BY ai.regTime DESC limit 15"

        result = cursor.execute(query)
        audition = cursor.fetchall()

        connection.commit()
        connection.close()
    except:
        connection.rollback()
        print('Faild DB Connection')


    return render(request, 'audition/index.html', {'cateType' : cate_type , 'subBanner' : subBanner, "recomAudi" : recomAudi, "finishAudi" : finishAudi, "audition": audition} )

#     /audi/audiDetail/(category)/(글번호)
def audi_detail(request, cate_type, num) :
    try :
        cursor = connection.cursor()

        user = request.session.get('id', '')

        if user:
            nowTime = timezone.now()
            saveView =  AuditionView.objects.create( auditionnum=num, userid=user, regtime=nowTime )
            updateView = AuditionInfo.objects.get(num=num)
            updateView.viewcount = updateView.viewcount + 1
            updateView.save()

            query = "SELECT ai.*, cm.cateName, uc.logoImage, uc.webSite, DATEDIFF(ai.auditionDate,  NOW()) AS diffDate, (SELECT COUNT(*) FROM audition_pick WHERE userID = '" + user + "' AND auditionNum = ai.num ) AS audiPick " \
                    "FROM audition_info AS ai LEFT JOIN cate_main AS cm ON ai.cate = cm.cateCode  " \
                    "     LEFT JOIN  user_company AS uc ON ai.userID = uc.userID  " \
                    "WHERE ai.num = '" + str(num) + "' limit 1"
        else:
            query = "SELECT ai.*, cm.cateName, uc.logoImage, uc.webSite, DATEDIFF(ai.auditionDate,  NOW()) AS diffDate, 0 as audiPick " \
                    "FROM audition_info AS ai LEFT JOIN cate_main AS cm ON ai.cate = cm.cateCode  " \
                    "     LEFT JOIN  user_company AS uc ON ai.userID = uc.userID  " \
                    "WHERE ai.num = '" + str(num) + "' limit 1"

        result = cursor.execute(query)
        audition = cursor.fetchall()

        audiSubCate = []
        for row in audition:
            subCate = row[4].split('|')
            image = row[15].split('|')
            print(row[28])
            for sub in subCate:
                cateName = CateSub.objects.get(subcate=sub)
                audiSubCate.append(cateName.catename)

        audiCate = ', '.join(audiSubCate)

        connection.commit()
        connection.close()
    except:
        connection.rollback()
        print('Faild DB Connection')

    return render(request, 'audition/viewer.html', {"audition": audition, "audiCate" : audiCate, "image" : image})


def audi_write(request) :

    cate = CateMain.objects.all().order_by('cateorder')

    return render(request, 'audition/write.html', {'cate':cate})


session = boto3.Session(
    aws_access_key_id = settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY,
)


def audi_write_callback(request) :

    userID = request.POST['userID']
    title = request.POST['title']
    cateMain = request.POST['cateMain']
    subCate = request.POST.getlist('subCate')
    startDate = request.POST.get('startDate',"9999-12-01 00:00:00")
    endDate = request.POST.get('endDate',"9999-12-01 00:00:00")
    ordinary = request.POST.get('ordinary', "0")
    auditionDate = request.POST.get('auditionDate',"9999-12-01")
    auditionTime = request.POST.get('auditionTime',"00:00:00")
    each = request.POST.get('each', "0")
    age = request.POST['age']
    gender = request.POST['gender']
    career = request.POST['career']
    essential = request.POST['essential']
    preparation = request.POST['preparation']

    catesub = "|".join(subCate) # subCate 문자열로 변환

    if ordinary == "1" :
        startDate = "9999-12-01 00:00:00"
        endDate = "9999-12-01 00:00:00"
        auditionDate = "9999-12-01"
        auditionTime = "00:00:00"

    userImage = request.FILES.getlist('userImage[]')

    print(userImage)

    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )

    nowTime = timezone.now()
    image = ""
    count = 0
    for image in userImage :
        count = count + 1
        sub = image.name.split('.')[-1]
        imgName = userID + "_" + image.name + "_" + str(nowTime)
        imageName = md5_generator(imgName) + "." + sub

        s3_client.upload_fileobj(
            image,
            settings.AWS_STORAGE_BUCKET_NAME,
            "media/photos/audition/image/" + imageName,
            ExtraArgs={
                "ContentType": image.content_type,
            }
        )

        if( count == 1) :
            imageURL = "photos/audition/image/" + imageName
        else :
            imageURL = imageURL + "|" + "photos/audition/image/" + imageName


    saveAudition = AuditionInfo.objects.create(userid=userID, title=title, cate=cateMain, subcate=catesub,
                                               startdate=startDate, enddate=endDate, ordinary=ordinary,
                                               auditiondate=auditionDate, auditiontime=auditionTime, each=each,
                                               age=age, gender=gender, career=career, image=imageURL, essential=essential,
                                               field_preparation=preparation, regtime=nowTime, viewcount=0, recorder=0, isdelete=0)

    key = str(AuditionInfo.objects.latest('num').num)

    return redirect('/audi/audiDetail/actor/'+key+"/")


def audiAjaxGetCate(request) :

    cate = request.GET.get('cate')
    catesub = CateSub.objects.filter(catecode=cate).order_by("cateorder")

    return render(request, 'audition/ajax_cate.html', {'catesub':catesub})