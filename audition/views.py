import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template import  loader
from django.db import connection

from picktalk.models import *
from django.conf import settings
from django.utils import timezone

from myonepick.common import *


# 오디션 /audi ...
#  -- 오디션 메인
#     /audi/main/actor/ : 배우 탭 활성화, 기본 탭.
#     /audi/main/model/ : 모델 탭 활성화
#     /audi/main/singer/ : 가수 탭 활성화
def audi_index(request, cate_type, page): # 오디션 Main
    try:
        cursor = connection.cursor()

        # 메인 베너
        subBanner = EventBanner.objects.filter(position="audi", nowview="1")

        user = request.session.get('id', '')

        if user:
            query = "SELECT AI.num, AI.title, AI.endDate, AI.ordinary, UC.logoImage, (SELECT COUNT(*) FROM audition_pick WHERE userID = '" + user + "' AND auditionNum = AI.num ) AS audiPick" \
                    " FROM audition_info AS AI LEFT JOIN user_company AS UC ON AI.userID  = UC.userID " \
                    "WHERE recommend = '1' and (AI.isDelete = '0' or AI.isDelete is null) " \
                    "order by AI.recOrder ASC, AI.regTime DESC "
        else:
            query = "SELECT AI.num, AI.title, AI.endDate, AI.ordinary, UC.logoImage, '0' AS audiPick" \
                    " FROM audition_info AS AI LEFT JOIN user_company AS UC ON AI.userID  = UC.userID " \
                    "WHERE recommend = '1' and (AI.isDelete = '0' or AI.isDelete is null) " \
                    "order by AI.recOrder ASC, AI.regTime DESC"

        result = cursor.execute(query)
        recomAudi = cursor.fetchall()

        if user:
            query = "SELECT AI.num, AI.title, AI.endDate, AI.ordinary, UC.logoImage, (SELECT COUNT(*) FROM audition_pick WHERE userID = '" + user + "' AND auditionNum = AI.num ) AS audiPick" \
                    " FROM audition_info AS AI LEFT JOIN user_company AS UC ON AI.userID  = UC.userID " \
                    "WHERE ordinary = '0' AND endDate >= NOW()  and (AI.isDelete = '0' or AI.isDelete is null) " \
                    "order by AI.endDate ASC LIMIT 4 "
        else:
            query = "SELECT AI.num, AI.title, AI.endDate, AI.ordinary, UC.logoImage, '0' AS audiPick " \
                    "FROM audition_info AS AI LEFT JOIN user_company AS UC ON AI.userID  = UC.userID " \
                    "WHERE ordinary = '0' AND endDate >= NOW() and (AI.isDelete = '0' or AI.isDelete is null) " \
                    "order by AI.endDate ASC LIMIT 4 "

        result = cursor.execute(query)
        finishAudi = cursor.fetchall()

        block = 15
        start = (page - 1) * block
        end = page * block

        print( start )
        print( end )

        query = "select * " \
                "FROM audition_info AS ai LEFT JOIN cate_main AS cm ON ai.cate = cm.cateCode " \
                "    LEFT JOIN  user_company AS uc ON ai.userID = uc.userID " \
                "where  ai.isDelete = '0' or ai.isDelete is null " \
                "ORDER BY ai.regTime DESC "

        result = cursor.execute(query)
        allList = cursor.fetchall()

        if user:
            query = "SELECT ai.num, ai.title, cm.cateName, ai.career, ai.age, ai.endDate, ai.regTime, ai.ordinary, uc.logoImage, DATEDIFF(NOW(),  ai.regTime) AS diffDate, (SELECT COUNT(*) FROM audition_pick WHERE userID = '" + user + "' AND auditionNum = ai.num ) AS audiPick, contentType, ai.cate " \
                    "FROM audition_info AS ai LEFT JOIN cate_main AS cm ON ai.cate = cm.cateCode " \
                    "    LEFT JOIN  user_company AS uc ON ai.userID = uc.userID " \
                    "where  ai.isDelete = '0' or ai.isDelete is null " \
                    "ORDER BY ai.regTime DESC limit " + str(start) + ", " + str(block)
        else:
            query = "SELECT ai.num, ai.title, cm.cateName, ai.career, ai.age, ai.endDate, ai.regTime, ai.ordinary, uc.logoImage, DATEDIFF(NOW(),  ai.regTime) AS diffDate , '0' AS audiPick, contentType, ai.cate " \
                    "FROM audition_info AS ai LEFT JOIN cate_main AS cm ON ai.cate = cm.cateCode " \
                    "    LEFT JOIN  user_company AS uc ON ai.userID = uc.userID " \
                    "where  ai.isDelete = '0' or ai.isDelete is null " \
                    "ORDER BY ai.regTime DESC limit " + str(start) + ", " + str(block)

        result = cursor.execute(query)
        audition = cursor.fetchall()

        allPage = (len(allList) / block) + 1
        paging = getPageList(page, allPage)

        connection.commit()
        connection.close()

    except:
        connection.rollback()

    return render(request, 'audition/index.html', {'cateType' : cate_type , 'subBanner' : subBanner, "recomAudi" : recomAudi,
                                                   "finishAudi" : finishAudi, "audition": audition, "paging" : paging, "page" : page } )


#     /audi/audiDetail/(category)/(글번호)
def audi_detail(request, cate_type, num) :

    user = request.session.get('id', '')

    audition = AuditionInfo.objects.get(num=num)
    companyInfo = UserCompany.objects.get(userid=audition.userid)

    if user:
        nowTime = timezone.now()
        saveView = AuditionView.objects.create(auditionnum=num, userid=user, regtime=nowTime)
        updateView = AuditionInfo.objects.get(num=num)
        updateView.viewcount = updateView.viewcount + 1
        updateView.save()

        userInfo = UserInfo.objects.get(userid=user)

        pick = AuditionPick.objects.filter(userid=user)
        if pick.count() == 0:
            pickCheck = "0"
        else:
            pickCheck = "1"

    else:
        pickCheck = "0"
        userInfo = ""

    images = audition.image.split("|")

    d_day = finalDate(audition.enddate)

    return render(request, 'audition/viewer.html', {"audition": audition, "companyInfo" : companyInfo, "image" : images
                                                    ,"userInfo": userInfo,"pickCheck": pickCheck, "D_day" : d_day})


def audi_write(request) :

    cate = CateMain.objects.all().order_by('cateorder')

    return render(request, 'audition/write.html', {'cate':cate})


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

    nowTime = timezone.now()
    imageURL = ""
    count = 0
    for image in userImage :
        count = count + 1
        sub = image.name.split('.')[-1]
        url = uploadFile(image,"photos/audition/image", sub)

        if( count == 1) :
            imageURL = url
        else :
            imageURL = imageURL + "|" +  url


    saveAudition = AuditionInfo.objects.create(userid=userID, title=title, cate=cateMain, subcate=catesub,
                                               startdate=startDate, enddate=endDate, ordinary=ordinary,
                                               auditiondate=auditionDate, auditiontime=auditionTime, each=each,
                                               age=age, gender=gender, career=career, image=imageURL, essential=essential,
                                               preparation=preparation, regtime=nowTime, viewcount=0, recorder=0, isdelete=0)

    key = str(AuditionInfo.objects.latest('num').num)

    return redirect('/audi/audiDetail/all/'+key+"/")


def audi_edit(request, num) :

    audition = AuditionInfo.objects.get(num=num)

    audisubCate = audition.subcate.split('|')
    cate = CateMain.objects.all()
    audiCate = CateSub.objects.filter(catecode=audition.cate)
    image = audition.image.split('|')

    return render(request, 'audition/edit.html', {"audition": audition, "cate" : cate, "audiCate" : audiCate,
                                                  "audisubCate" : audisubCate, "image":image})

def audi_edit_callback( request ) :
    userID = request.POST['userID']
    num = request.POST['num']
    title = request.POST['title']
    cateMain = request.POST['cateMain']
    subCate = request.POST.getlist('subCate')
    startDate = request.POST.get('startDate', "9999-12-01 00:00:00")
    endDate = request.POST.get('endDate', "9999-12-01 00:00:00")
    ordinary = request.POST.get('ordinary', "0")
    auditionDate = request.POST.get('auditionDate', "9999-12-01")
    auditionTime = request.POST.get('auditionTime', "00:00:00")
    each = request.POST.get('each', "0")
    age = request.POST['age']
    gender = request.POST['gender']
    career = request.POST['career']
    essential = request.POST['essential']
    preparation = request.POST['preparation']
    removeImage = request.POST.get('removeImage', "")

    catesub = "|".join(subCate)  # subCate 문자열로 변환

    if ordinary == "1":
        startDate = "9999-12-01 00:00:00"
        endDate = "9999-12-01 00:00:00"
        auditionDate = "9999-12-01"
        auditionTime = "00:00:00"

    userImage = request.FILES.getlist('userImage[]')

    # 이미지 등록.
    nowTime = timezone.now()

    addImage = []
    for image in userImage:
        sub = image.name.split('.')[-1]
        url = uploadFile(image, "photos/audition/image", sub) # 파일 업로드

        addImage.append(url)

    updateAudition = AuditionInfo.objects.get(num = num)

    # DB에서 이미지 저장된 내용 빼기.
    dbImage = updateAudition.image.split('|')

    # 이미지 삭제.
    rmImage = removeImage.split('|')
    if( removeImage != "") :
      for rmImages in rmImage :
         if( rmImages == ""): continue
         deleteFile(rmImages)
         dbImage.remove(rmImages)


    saveImage = dbImage + addImage
    imageUrl = "|".join(saveImage)

    updateAudition.title = title
    updateAudition.cate = cateMain
    updateAudition.subcate = catesub
    updateAudition.startdate = startDate
    updateAudition.enddate = endDate
    updateAudition.ordinary = ordinary
    updateAudition.auditiondate = auditionDate
    updateAudition.auditiontime = auditionTime
    updateAudition.each = each
    updateAudition.age = age
    updateAudition.gender = gender
    updateAudition.career = career
    updateAudition.image = imageUrl
    updateAudition.essential = essential
    updateAudition.field_preparation = preparation
    updateAudition.updtime = nowTime

    updateAudition.save()

    return redirect('/audi/audiDetail/all/' + num + "/")

def audi_delete(request, num):
    updateAudition = AuditionInfo.objects.get(num=num)
    updateAudition.isdelete = '1'
    updateAudition.save()

    return redirect('/audi/main/all/')

def audiAjaxGetCate(request) :

    cate = request.GET.get('cate')
    catesub = CateSub.objects.filter(catecode=cate).order_by("cateorder")

    return render(request, 'audition/ajax_cate.html', {'catesub':catesub})



def audiApply(request) :

    profileCheck = request.GET['profileCheck']
    num = request.GET['num']
    writeUID = request.GET['writeUID']
    userID = request.GET['userID']

    nowTime = timezone.now()

    saveApply = AuditionApply.objects.create( auditionnum=num, profilenum=profileCheck, regtime=nowTime)

    return JsonResponse({"code": "0"})