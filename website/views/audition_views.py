from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db import connection

from picktalk.models import *
from django.utils import timezone

from myonepick.common import *
from django.views.decorators.csrf import requires_csrf_token


# 오디션 /audi ...
#  -- 오디션 메인
#     /audi/main/actor/ : 배우 탭 활성화, 기본 탭.
#     /audi/main/model/ : 모델 탭 활성화
#     /audi/main/singer/ : 가수 탭 활성화
def audi_index(request): # 오디션 Main3
    nUrl = nowDevice(request)

    cate_type = request.GET.get("cate_type", "recomend")
    page = int( request.GET.get("page", "1") )
    searchWord = request.GET.get("search", "")

    block = 10
    start = (page - 1) * block
    end = page * block

    where = ""
    if searchWord != "" :
        where = " and ( title like '%"+searchWord+"%' or essential like '%"+searchWord+"%' or preparation like '%"+searchWord+"%' )"


    try:
        cursor = connection.cursor()

        user = request.session.get('id', '')

        query = "select ai.num " \
                "FROM audition_info AS ai " \
                "where  (ai.isDelete = '0' or ai.isDelete is null ) " + where + " "

        result = cursor.execute(query)
        allList = cursor.fetchall()

        if cate_type  == "recomend" :

            if user:
                query = "SELECT ai.num, ai.title, ai.cate, ai.subcate, ai.career, ai.age, ai.gender, ai.endDate, ai.ordinary, (SELECT COUNT(*) FROM audition_pick WHERE userID = '" + user + "' AND auditionNum = ai.num ) AS audiPick, contentType, ai.image ,  DATEDIFF(NOW(), endDate) AS diffDate, regTime " \
                        "FROM audition_info AS ai  " \
                        "where  (ai.isDelete = '0' or ai.isDelete is null ) " + where + " " \
                        "ORDER BY recommend DESC, regTime DESC limit " + str(start) + ", " + str(block)

            else:
                query = "SELECT ai.num, ai.title, ai.cate, ai.subcate, ai.career, ai.age, ai.gender, ai.endDate, ai.ordinary, '0' AS audiPick, contentType, ai.image,  DATEDIFF(NOW(), endDate) AS diffDate, regTime " \
                        "FROM audition_info AS ai " \
                        "where  (ai.isDelete = '0' or ai.isDelete is null ) " + where + " " \
                        "ORDER BY recommend DESC, regTime DESC limit " + str(start) + ", " + str(block)

        elif cate_type == "new" :
            if user:
                query = "SELECT ai.num, ai.title, ai.cate, ai.subcate, ai.career, ai.age, ai.gender, ai.endDate, ai.ordinary, (SELECT COUNT(*) FROM audition_pick WHERE userID = '" + user + "' AND auditionNum = ai.num ) AS audiPick, contentType, ai.image ,  DATEDIFF(NOW(), endDate) AS diffDate, regTime " \
                        "FROM audition_info AS ai  " \
                        "where  (ai.isDelete = '0' or ai.isDelete is null ) " + where + " " \
                        "ORDER BY ai.regTime DESC limit " + str(start) + ", " + str(block)

            else:
                query = "SELECT ai.num, ai.title, ai.cate, ai.subcate, ai.career, ai.age, ai.gender, ai.endDate, ai.ordinary, '0' AS audiPick, contentType, ai.image,  DATEDIFF(NOW(), endDate) AS diffDate, regTime " \
                        "FROM audition_info AS ai " \
                        "where  (ai.isDelete = '0' or ai.isDelete is null ) " + where + " " \
                        "ORDER BY ai.regTime DESC limit " + str(start) + ", " + str(block)

        else :
            if user:
                query = "SELECT * " \
                        "FROM ( SELECT ai.num, ai.title, ai.cate, ai.subcate, ai.career, ai.age, ai.gender, ai.endDate, ai.ordinary, (SELECT COUNT(*) FROM audition_pick WHERE userID = '" + user + "' AND auditionNum = ai.num ) AS audiPick, contentType, ai.image,  DATEDIFF(NOW(), endDate) AS diffDate, regTime " \
                        "       FROM audition_info AS ai" \
                        "	WHERE  (ai.isDelete = '0' OR ai.isDelete IS NULL )  " + where + "  ) AS B " \
                        "ORDER BY (CASE WHEN diffDate <= 0 AND diffDate >= -100 THEN diffDate END) DESC, (CASE WHEN diffDate  > 0 THEN regTime END) DESC limit " + str(start) + ", " + str(block)

            else:
                query = "SELECT * " \
                        "FROM ( SELECT ai.num, ai.title, ai.cate, ai.subcate, ai.career, ai.age, ai.gender, ai.endDate, ai.ordinary, '0' AS audiPick, contentType, ai.image,  DATEDIFF(NOW(), endDate) AS diffDate, regTime " \
                        "       FROM audition_info AS ai" \
                        "	WHERE  (ai.isDelete = '0' OR ai.isDelete IS NULL )  " + where + "  ) AS B " \
                        "ORDER BY (CASE WHEN diffDate <= 0 AND diffDate >= -100 THEN diffDate END) DESC, (CASE WHEN diffDate  > 0 THEN regTime END) DESC limit " + str(start) + ", " + str(block)

        print(query)


        result = cursor.execute(query)
        audition = cursor.fetchall()

        allPage = int(len(allList) / block) + 1
        paging = getPageList_v2(page, allPage)

        connection.commit()
        connection.close()

    except:
        connection.rollback()

    return render(request, nUrl + '/audition/index.html',
                  {'cateType' : cate_type , "audition": audition, "paging" : paging, "page" : page,
                   "leftPage": page - 1, "rightPage": page + 1, "lastPage": allPage, "searchWord" : searchWord })


#     /audi/audiDetail/(category)/(글번호)
def audi_detail(request, cate_type, num) :
    nUrl = nowDevice(request)

    user = request.session.get('id', '')

    audition = AuditionInfo.objects.get(num=num)
    companyInfo = UserCompany.objects.get(userid=audition.userid)
    userInfo2 = UserInfo.objects.get(userid=audition.userid)

    if user:
        nowTime = timezone.now()
        saveView = AuditionView.objects.create(auditionnum=num, userid=user, regtime=nowTime)
        updateView = AuditionInfo.objects.get(num=num)
        updateView.viewcount = updateView.viewcount + 1
        updateView.save()

        userInfo = UserInfo.objects.get(userid=user)

        pick = AuditionPick.objects.filter(userid=user, auditionnum=num)
        if pick.count() == 0:
            pickCheck = "0"
        else:
            pickCheck = "1"

        data1 = ProfileInfo.objects.filter(userid=user, isdelete=0)

    else:
        pickCheck = "0"
        userInfo = ""

        data1 = ""

    images = audition.image.split("|")

    d_day = finalDate(audition.enddate)

    return render(request, nUrl + '/audition/viewer.html', {"audition": audition, "companyInfo" : companyInfo, "userInfo2" : userInfo2, "image" : images
                                                    ,"userInfo": userInfo,"pickCheck": pickCheck, "D_day" : d_day, "data1" : data1})

@requires_csrf_token
def audi_write(request) :

    nUrl = nowDevice(request)

    user = request.session.get('id', '')

    if user == "" or user == None :
        message = '로그인 후 이용가능합니다..'
        return HttpResponse("<script>alert('" + message + "'); window.location.href = '/'; </script>")


    cate = CateMain.objects.all().order_by('cateorder')
    catesub = CateSub.objects.filter(catecode="mainCate1").order_by("cateorder")

    return render(request, nUrl + '/audition/write.html', {'cate':cate, "catesub" : catesub})

@requires_csrf_token
def audi_write_callback(request) :

    nUrl = nowDevice(request)

    userID = request.POST['userID']
    title = request.POST['title']
    cateMain = request.POST['cateMain']
    subCate = request.POST.getlist('subCate')
    startDate = request.POST.get('startDate',"9999-12-01 00:00:00")
    endDate = request.POST.get('endDate',"9999-12-01 00:00:00")
    ordinary = request.POST.get('ordinary', "0")
    auditionDate = request.POST.get('auditionDate',"9999-12-01")
    notAudi = request.POST.get('notAudi', "0")
    each = request.POST.get('each', "0")
    age = request.POST.get('age',"")
    gender = request.POST.get('gender',"")
    career = request.POST.get('career',"")
    essential = request.POST.get('essential',"")
    preparation = request.POST.get('preparation',"")

    catesub = "|".join(subCate) # subCate 문자열로 변환

    if ordinary == "1" :
        startDate = "9999-12-01 00:00:00"
        endDate = "9999-12-01 00:00:00"

    if notAudi == "1" :
        auditionDate = "9999-12-01"

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

    logoImage = request.FILES.getlist('logoImage[]')
    logoUrl = ""
    count = 0
    for image in logoImage:
        count = count + 1
        sub = image.name.split('.')[-1]
        logoUrl = uploadFile(image, "photos/audition/image", sub)

    saveAudition = AuditionInfo.objects.create(userid=userID, title=title, cate=cateMain, subcate=catesub,
                                               startdate=startDate, enddate=endDate, ordinary=ordinary,
                                               auditiondate=auditionDate, audiunsetted=notAudi, each=each, logo_image=logoUrl,
                                               age=age, gender=gender, career=career, image=imageURL, essential=essential,
                                               preparation=preparation, regtime=nowTime, viewcount=0, recorder=0, isdelete=0)

    key = str(AuditionInfo.objects.latest('num').num)

    return redirect('/audi/audiDetail/all/'+key+"/")


def audi_edit(request, num) :
    nUrl = nowDevice(request)

    user = request.session.get('id', '')

    if user == "" or user == None :
        message = '로그인 후 이용가능합니다..'
        return HttpResponse("<script>alert('" + message + "'); window.location.href = '/'; </script>")

    audition = AuditionInfo.objects.get(num=num)

    audisubCate = audition.subcate.split('|')
    cate = CateMain.objects.all()
    audiCate = CateSub.objects.filter(catecode=audition.cate)
    image = audition.image.split('|')

    return render(request, nUrl + '/audition/edit.html', {"audition": audition, "cate" : cate, "audiCate" : audiCate,
                                                  "audisubCate" : audisubCate, "image":image})

def audi_edit_callback( request ) :
    nUrl = nowDevice(request)

    num = request.POST['num']
    title = request.POST['title']
    cateMain = request.POST['cateMain']
    subCate = request.POST.getlist('subCate')
    startDate = request.POST.get('startDate',"9999-12-01 00:00:00")
    endDate = request.POST.get('endDate',"9999-12-01 00:00:00")
    ordinary = request.POST.get('ordinary', "0")
    auditionDate = request.POST.get('auditionDate',"9999-12-01")
    notAudi = request.POST.get('notAudi', "0")
    each = request.POST.get('each', "0")
    age = request.POST.get('age',"")
    gender = request.POST.get('gender',"")
    career = request.POST.get('career',"")
    essential = request.POST.get('essential',"")
    preparation = request.POST.get('preparation',"")
    removeImage = request.POST.get('removeImage', "")

    catesub = "|".join(subCate)  # subCate 문자열로 변환

    if ordinary == "1":
        startDate = "9999-12-01 00:00:00"
        endDate = "9999-12-01 00:00:00"

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
    if updateAudition.image :
        dbImage = updateAudition.image.split('|')
    else :
        dbImage = []

    # 이미지 삭제.
    rmImage = removeImage.split('|')
    if( removeImage != "") :
      for rmImages in rmImage :
         if( rmImages == ""): continue
         deleteFile(rmImages)
         dbImage.remove(rmImages)


    saveImage = dbImage + addImage
    imageUrl = "|".join(saveImage)


    logoImage = request.FILES.getlist('logoImage[]')
    logoUrl = updateAudition.logo_image
    count = 0
    if logoImage :
        if logoUrl :
            deleteFile(logoUrl)

        for image in logoImage:
            count = count + 1
            sub = image.name.split('.')[-1]
            logoUrl = uploadFile(image, "photos/audition/image", sub)

    updateAudition.title = title
    updateAudition.cate = cateMain
    updateAudition.subcate = catesub
    updateAudition.startdate = startDate
    updateAudition.enddate = endDate
    updateAudition.ordinary = ordinary
    updateAudition.auditiondate = auditionDate
    updateAudition.audiunsetted = notAudi
    updateAudition.each = each
    updateAudition.age = age
    updateAudition.gender = gender
    updateAudition.career = career
    updateAudition.image = imageUrl
    updateAudition.essential = essential
    updateAudition.preparation = preparation
    updateAudition.updtime = nowTime
    updateAudition.logo_image = logoUrl

    updateAudition.save()

    userType = request.session['userType']
    if userType == "admin":
        nowTime = str(timezone.now())
        user = request.session.get('id', '')
        adminLog = AdminLog.objects.create(userid=user, viewtype="audition_edit", content=num, regdate=nowTime)

    return redirect('/audi/audiDetail/all/' + num + "/")

def audi_delete(request, num):
    nUrl = nowDevice(request)

    updateAudition = AuditionInfo.objects.get(num=num)
    updateAudition.isdelete = '1'
    updateAudition.save()

    userType = request.session['userType']
    if userType == "admin":
        nowTime = str(timezone.now())
        user = request.session.get('id', '')
        adminLog = AdminLog.objects.create(userid=user, viewtype="audition_del", content=num, regdate=nowTime)

    return redirect('/audi/list/')

def audiAjaxGetCate(request) :
    nUrl = nowDevice(request)

    cate = request.GET.get('cate')
    catesub = CateSub.objects.filter(catecode=cate).order_by("cateorder")

    return render(request, nUrl + '/audition/ajax_cate.html', {'catesub':catesub})



def audiApply(request) :

    profileCheck = request.GET['profileCheck']
    num = request.GET['num']
    writeUID = request.GET['writeUID']
    userID = request.GET['userID']

    findApply = AuditionApply.objects.filter(auditionnum=num, profilenum=profileCheck)

    if findApply.count() > 0 :
        return JsonResponse({"code": "1", "msg" : "이미 지원하셨습니다."})

    nowTime = timezone.now()

    saveApply = AuditionApply.objects.create( auditionnum=num, profilenum=profileCheck, regtime=nowTime)

    return JsonResponse({"code": "0"})