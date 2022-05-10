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
    """
    try:
        if cate_type == 'actor':
            cate = '2'
        elif cate_type == 'model' :
            cate = '3'
        elif cate_type == 'singer' :
            cate = '4'

        newAudi = Audition.objects.filter( subCategories__category__id=cate ).distinct().order_by('-regTime')[:4] # 신규오디션.

        today = datetime.now()  # 오늘날짜
        finishAudi = Audition.objects.filter( endDate__gte = today, subCategories__category__id=cate ).distinct().order_by('endDate')[:4] # 마감임박 오디션.

        recomAudi = Audition.objects.filter( subCategories__category__id=cate ).distinct().order_by('-id')[:4] # 추천 오디션.  --> 출력 순서 확인 필요.
    except:
        connection.rollback()
        print('Faild DB Connection')


    return render(request, 'audition/index.html', {'cateType' : cate_type , 'newAudi' : newAudi, "finishAudi" : finishAudi, "recomAudi": recomAudi} )
    """

    return render(request, 'audition/index.html' )

#     /audi/audiDetail/(category)/(글번호)
def audi_detail(request, cate_type, num) :
    """
    try:
        audiViewData = Audition.objects.filter(id=num) # 오디션 기본 정보.
        viewImages = AuditionImages.objects.filter(audition__id=num) # 본문 이미지

        category_actor = AuditionSubCategory.objects.filter(category=2, audition__id=num)
        category_model = AuditionSubCategory.objects.filter(category=3, audition__id=num)
        category_singer = AuditionSubCategory.objects.filter(category=4, audition__id=num)
    except:
        connection.rollback()
        print('Faild DB Connection')

    return render(request, 'audition/viewer.html', { "cateType" : cate_type , "audiViewData" : audiViewData , "viewImages" : viewImages
        , "category_actor" : category_actor, "category_model" : category_model, "category_singer" : category_singer } )
    """

    return render(request, 'audition/viewer.html')


def audi_write(request) :

    cate = CateMain.objects.all().order_by('cateorder')
    catesub = CateSub.objects.filter(catecode="mainCate1").order_by("cateorder")

    return render(request, 'audition/write.html', {'cate':cate, 'catesub' : catesub})


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
    auditionDate = request.POST['auditionDate']
    auditionTime = request.POST['auditionTime']
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
            imageURL = "media/photos/audition/image/" + imageName
        else :
            imageURL = imageURL + "|" + "media/photos/audition/image/" + imageName


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