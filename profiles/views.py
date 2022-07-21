from django.shortcuts import render, redirect
from picktalk.models import *
import datetime
from django.utils import timezone
from django.conf import settings
import hashlib
from audition.views import md5_generator
from django.http import HttpResponse, JsonResponse
from django.db import connection
from myonepick.common import *


# Create your views here.
# profile/list/actor/ -- 배우 리스트
# profile/list/model/ -- 모델 리스트
# profile/list/singer/ -- 가수 리스트
# profile/list/dancer/ -- 댄서 리스트
# profile/list/influencer/ -- 인플루언서 리스트

# 4번째 인자
#  - newest : 최신순
#  - popular : 인기순
#  - share : 공유
#  - recommend : 추천

def orderbyType(orderby):
    if orderby == 'newest' :
        orderName = '-regTime'
    elif orderby== 'popular' :
        orderName = '-regTime'
    elif orderby== 'share' :
        orderName = '-regTime'
    elif orderby== 'recommend' :
        orderName = '-regTime'
    return orderName

def getCateType(cate_type):
    if cate_type == 'actor':
        cate = '2'
    elif cate_type == 'model' :
        cate = '3'
    elif cate_type == 'singer' :
        cate = '4'
    return cate


def listView(request, cate_type, page): # 오디션 Main

    try:
        cursor = connection.cursor()

        user = request.session.get('id', '')

        intercate = ""
        if cate_type == "actor" :
            intercate = " and ( p.interCate = 'mainCate1' || p.interCate like '%배우%' ) "
        elif cate_type == "model" :
            intercate = " and ( p.interCate = 'mainCate2' || p.interCate like '%배우%' ) "
        elif cate_type == "singer" :
            intercate = " and ( p.interCate = 'mainCate3' || p.interCate like '%가수%' ) "

        # 프로필
        if user:
            query = "SELECT p.num , profileImage, height, weight, viewCount, pickCount, cViewCount, ui.name, ui.birth, ui.entertain, " \
                    "       ui.gender, ui.military, ui.school, ui.major, talent, comment, mainYoutube, isCareer, (SELECT COUNT(*) FROM profile_pick WHERE userID = '" + user + "' AND profileNum = p.num ) AS proPick " \
                    "FROM profile_info AS p LEFT JOIN user_info AS ui  ON p.userID = ui.userID " \
                    "WHERE public = '0' and isDelete = '0'  and ui.userID != '' " + intercate + " " \
                    "ORDER BY `upDate` Desc, regDate DESC " \
                    "LIMIT 10"
        else:
            query = "SELECT p.num, profileImage, height, weight, viewCount, pickCount, cViewCount, ui.name, ui.birth, ui.entertain," \
                    "       ui.gender, ui.military, ui.school, ui.major, talent, comment, mainYoutube, isCareer, '0' AS proPick " \
                    "FROM profile_info AS p LEFT JOIN user_info AS ui " \
                    "     ON p.userID = ui.userID " \
                    "WHERE public = '0' and isDelete = '0'  and ui.userID != '' " + intercate + " " \
                    "ORDER BY `upDate` Desc, regDate DESC  " \
                    "LIMIT 10"

        result = cursor.execute(query)
        profiles = cursor.fetchall()

        connection.commit()
        connection.close()

    except:
        connection.rollback()
    return render(request, 'profiles/list.html', { 'profiles':profiles, "cateType" : cate_type, "page" : page })


def viewer(request, cate_type, num) :

    #프로필 정보.
    profiles = ProfileInfo.objects.get(num=num)
    writeUser = profiles.userid

    #프로필 등록자 정보
    userInfo = UserInfo.objects.get(userid=writeUser)
    careerEtc = ProfileEtccareer.objects.filter(profilenum=num).order_by("num")
    comment = ProfileComment.objects.filter(profilenum=num).order_by("-num")

    user = request.session.get('id', '')
    if user :
        pick = ProfilePick.objects.filter(userid=user, profilenum=num)
        if pick.count() == 0 :
            pickCheck = "0"
        else :
            pickCheck = "1"

    else :
        pickCheck = "0"

    if (profiles.detailimage):
        profileImages = profiles.detailimage.split("|")
    else:
        profileImages = ""

    if(  profiles.artimage ) :
        artImages = profiles.artimage.split("|")
    else :
        artImages = ""

    youtubes = profiles.youtube.split("|")
    foreign = profiles.foreign.split("|")

    if (profiles.talent):
        talent = profiles.talent.split("|")
    else :
        talent = ""

    # 세부 분야별 경력정보
    movieCareer = getCareerList(num, "movie")
    dramaCareer = getCareerList(num, "drama")
    etcCareer = getCareerList(num, "etc")

    userType = request.session.get('userType', '')

    nowTime = timezone.now()

    if userType == "COMPANY" or userType == "S-COMPANY" :
        userID = request.session.get('id', '')
        profiles.cviewcount = profiles.cviewcount + 1
        profiles.save()
        viewAdd = ProfileViewCompany.objects.create(profilenum=num, userid=user, regtime=nowTime)

        audiList = AuditionInfo.objects.filter(userid=userID, isdelete="0")

    else :
        profiles.viewcount = profiles.viewcount +1
        profiles.save()
        viewAdd = ProfileView.objects.create(profilenum=num, userid=user, regtime=nowTime)
        audiList = ""
    

    return render(request, 'profiles/viewer.html', { 'profiles':profiles, "userInfo":userInfo, "foreign" : foreign,
                                                     "careerEtc":careerEtc, "comment":comment, "pickCheck" : pickCheck,
                                                     "profileImages" : profileImages, "artImages" : artImages,
                                                     "youtubes" : youtubes, "movieCareer" : movieCareer, "dramaCareer" : dramaCareer,
                                                     "etcCareer": etcCareer, "talent" : talent, "audiList" : audiList})


def viewer_all(request, cate_type, num):
    # 프로필 정보.
    profiles = ProfileInfo.objects.get(num=num)
    writeUser = profiles.userid

    # 프로필 등록자 정보
    userInfo = UserInfo.objects.get(userid=writeUser)
    careerEtc = ProfileEtccareer.objects.filter(profilenum=num).order_by("num")
    comment = ProfileComment.objects.filter(profilenum=num).order_by("-num")

    user = request.session.get('id', '')
    if user:
        pick = ProfilePick.objects.filter(userid=user)
        if pick.count() == 0:
            pickCheck = "0"
        else:
            pickCheck = "1"

    else:
        pickCheck = "0"

    if (profiles.detailimage):
        profileImages = profiles.detailimage.split("|")
    else:
        profileImages = ""

    if (profiles.artimage):
        artImages = profiles.artimage.split("|")
    else:
        artImages = ""

    youtubes = profiles.youtube.split("|")
    foreign = profiles.foreign.split("|")

    if (profiles.talent):
        talent = profiles.talent.split("|")
    else:
        talent = ""

    # 세부 분야별 경력정보
    movieCareer = getCareerList(num, "movie")
    dramaCareer = getCareerList(num, "drama")
    etcCareer = getCareerList(num, "etc")

    userType = request.session.get('userType', '')

    nowTime = timezone.now()

    if userType == "COMPANY" or userType == "S-COMPANY":
        userID = request.session.get('id', '')
        profiles.cviewcount = profiles.cviewcount + 1
        profiles.save()
        viewAdd = ProfileViewCompany.objects.create(profilenum=num, userid=user, regtime=nowTime)

        audiList = AuditionInfo.objects.filter(userid=userID, isdelete="0")

    else:
        profiles.viewcount = profiles.viewcount + 1
        profiles.save()
        viewAdd = ProfileView.objects.create(profilenum=num, userid=user, regtime=nowTime)
        audiList = ""

    return render(request, 'profiles/viewer_all.html', {'profiles': profiles, "userInfo": userInfo, "foreign": foreign,
                                                    "careerEtc": careerEtc, "comment": comment, "pickCheck": pickCheck,
                                                    "profileImages": profileImages, "artImages": artImages,
                                                    "youtubes": youtubes, "movieCareer": movieCareer,
                                                    "dramaCareer": dramaCareer,
                                                    "etcCareer": etcCareer, "talent": talent, "audiList": audiList})


def pofile_write(request) :

    userID = request.session['id']
    user = UserInfo.objects.get(userid=userID)
    cate = CateMain.objects.all()

    checkProfile = ProfileInfo.objects.filter(userid=userID)

    return render(request, 'profiles/write.html', { 'user':user, 'cate' : cate, "checkProfile" : checkProfile })

def pofile_write_callback(request) :

    # 기본정보
    userID = request.POST['userID']
    nationality = request.POST['nationality']
    military = request.POST['military']
    entertain = request.POST['entertain']
    finalSchool = request.POST['finalSchool']
    school = request.POST['school']
    major = request.POST['major']
    instagram = request.POST['instagram']
    youtube = request.POST['youtube']

    #신체정보
    height = request.POST['height']
    weight = request.POST['weight']
    topSize = request.POST['topSize']
    bottomSize = request.POST['bottomSize']
    shoesSize = request.POST['shoesSize']
    skinColor = request.POST['skinColor']
    hairColor = request.POST['hairColor']

    #지원 분야
    cate_m = request.POST['cate_m']
    cate_s = request.POST['cate_s']

    # 경력
    notCareer = request.POST.get('notCareer',"0")
    saveCareer = request.POST['saveCareer'] # 경력 리스트 '|' 구분
    allCareer_y = request.POST.get('allCareer_y')
    allCareer_m = request.POST.get('allCareer_m')

    # 이미지
    mainImage = request.FILES.getlist('mainImage[]')
    profileImage = request.FILES.getlist('profileImage[]')
    userImage = request.FILES.getlist('userImage[]')

    # 프로필 영상.
    mainYoutube = request.POST.get('mainYoutube',"0")
    youSave = request.POST['youSave']

    youtubes = youSave.split('|')
    saveYoutube = []
    youtube_main = ''
    if youSave != "" :
        for you in youtubes :
            tube = you.split('$')
            if tube[0] == mainYoutube :
                youtube_main = tube[1]
            saveYoutube.append(tube[1])
    sYoutube = "|".join(saveYoutube)

    #기타
    etcSaveCareer = request.POST.get('etcSaveCareer')
    saveForeign = request.POST['saveForeign']
    saveSpecialty = request.POST['saveSpecialty']
    introduction = request.POST['introduction']
    notView = request.POST.get('notView',"0")

    nowTime = timezone.now()

    image_main = ""
    count = 0
    # 메인 이미지 등록
    for image in mainImage:
        count = count + 1
        sub = image.name.split('.')[-1]
        url = uploadFile(image, "photos/profiles/main/", sub)

        image_main = url

    # 프로필 이미지 등록.
    image_profile = ""
    if len(profileImage) != 0 :
        count = 0
        for image in profileImage:
            count = count + 1
            sub = image.name.split('.')[-1]
            url = uploadFile(image, "photos/profile/additional/", sub)

            if (count == 1):
                image_profile = url
            else:
                image_profile = image_profile + "|" + url

    image_act = ""
    if len(userImage) != 0 :
        count = 0
        for image in userImage:
            count = count + 1
            sub = image.name.split('.')[-1]
            url = uploadFile(image, "photos/profile/additional/", sub)

            if (count == 1):
                image_act = url
            else:
                image_act = url

    # 기본정보 수정.
    userInfo = UserInfo.objects.get(userid=userID)
    userInfo.nationality = nationality;
    userInfo.military = military;
    userInfo.entertain = entertain;
    userInfo.finalschool = finalSchool;
    userInfo.school = school;
    userInfo.major = major;
    userInfo.instargram = instagram;
    userInfo.youtube = youtube;
    userInfo.save();

    nowTime = timezone.now()

    saveProfile = ProfileInfo.objects.create(userid=userID, profileimage=image_main, detailimage=image_profile, artimage=image_act,
                                             height=height, weight=weight, topsize=topSize, bottomsize=bottomSize, shoessize=shoesSize,
                                             skincolor=skinColor, haircolor=hairColor, foreign=saveForeign, mainyoutube=youtube_main,
                                             youtube=sYoutube, talent=saveSpecialty, comment=introduction, intercate=cate_m,
                                             intersubcate=cate_s, iscareer=notCareer, careeryear=allCareer_y, careermonth=allCareer_m,
                                             regdate=nowTime, viewcount=0, cviewcount=0, public=notView,isdelete=0, pickcount=0 )

    key = str(ProfileInfo.objects.latest('num').num)

    if notCareer == "0" :
        career = saveCareer.split('|')
        for careers in career :
            #c_cateM_val + "$" + c_cateM + "$" + c_cateS_val + "$" + c_cateS + "$" + c_title + "$" + c_role
            careerContent = careers.split('$')
            saveProCareer = ProfileCareer.objects.create(userid=userID, profilenum=key, catetype=careerContent[0],catesubtype=careerContent[2],
                                                         title=careerContent[4], role=careerContent[5], regtime=nowTime)

    if etcSaveCareer != "" :
        etcCareer = etcSaveCareer.split('|')
        for careers in etcCareer :
            #ec_cateM + "$" + ec_cateS + "$" + ec_title + "$" + ec_role;
            careerContent = careers.split('$')
            saveProCareerEtc = ProfileEtccareer.objects.create(userid=userID, profilenum=key, catetype=careerContent[0],subcatetype=careerContent[1],
                                                               title=careerContent[2], role=careerContent[3], regtime=nowTime)

    return redirect('/profile/profileDetail/all/' + key + "/")


def pofile_edit(request, num) :

    userID = request.session['id']
    profiles = ProfileInfo.objects.get(num=num)
    user = UserInfo.objects.get(userid=profiles.userid)
    cate = CateMain.objects.all()
    catesub = CateSub.objects.filter(catecode=profiles.intercate).order_by("cateorder")

    cursor = connection.cursor()

    query = "SELECT profileNum, title, ROLE, cm.cateName AS mainCate, cs.cateName AS subCate, cateType, cateSubType  " \
            "FROM profile_career AS pc LEFT JOIN cate_main AS cm ON pc.cateType = cm.cateCode " \
            "     LEFT JOIN cate_sub AS cs ON pc.cateSubType = cs.subCate " \
            "WHERE pc.profileNum = '" + str(num) + "' order by pc.num asc "

    result = cursor.execute(query)
    careerList = cursor.fetchall()

    connection.commit()
    connection.close()

    if profiles.detailimage != None :
        profileImages = profiles.detailimage.split("|")
    else :
        profileImages = ""

    if profiles.artimage != None :
        artImages = profiles.artimage.split("|")
    else :
        artImages = ""

    if profiles.youtube != None :
        youtubes = profiles.youtube.split("|")
    else :
        youtubes = ""

    if profiles.foreign != None :
        foreign = profiles.foreign.split("|")
    else :
        foreign = ""

    if profiles.talent != None :
        talent = profiles.talent.split("|")
    else :
        talent = ""

    careerEtc = ProfileEtccareer.objects.filter(profilenum=num).order_by("num")

    return render(request, 'profiles/edit.html', { 'user':user, 'cate' : cate, 'num' : num, 'profiles' : profiles,
                                                   'catesub':catesub, "careerList" : careerList, "profileImages" : profileImages,
                                                   "artImages":artImages, "youtubes":youtubes, "foreign": foreign, "talent": talent,
                                                   "careerEtc":careerEtc})


def pofile_edit_callback(request) :
    # 기본정보
    num = request.POST['num']

    profiles = ProfileInfo.objects.get(num=num)

    userID = profiles.userid
    nationality = request.POST['nationality']
    military = request.POST['military']
    entertain = request.POST['entertain']
    finalSchool = request.POST['finalSchool']
    school = request.POST['school']
    major = request.POST['major']
    instagram = request.POST['instagram']
    youtube = request.POST['youtube']

    # 신체정보
    height = request.POST['height']
    weight = request.POST['weight']
    topSize = request.POST['topSize']
    bottomSize = request.POST['bottomSize']
    shoesSize = request.POST['shoesSize']
    skinColor = request.POST['skinColor']
    hairColor = request.POST['hairColor']

    # 지원 분야
    cate_m = request.POST['cate_m']
    cate_s = request.POST['cate_s']

    # 경력
    notCareer = request.POST.get('notCareer', "0")
    saveCareer = request.POST['saveCareer']  # 경력 리스트 '|' 구분
    allCareer_y = request.POST.get('allCareer_y', "")
    allCareer_m = request.POST.get('allCareer_m', "")

    # 이미지
    mainImage = request.FILES.getlist('mainImage[]')
    profileImage = request.FILES.getlist('profileImage[]')
    userImage = request.FILES.getlist('userImage[]')
    mainImg = request.POST.get('mainImg', "")


    removeImage_detail = request.POST.get('removeImage_detail', "")
    removeImage_art = request.POST.get('removeImage_art', "")

    # 프로필 영상.
    mainYoutube = request.POST.get('mainYoutube', "0")
    youSave = request.POST['youSave']

    youtubes = youSave.split('|')
    saveYoutube = []
    youtube_main = ''
    if youSave != "":
        for you in youtubes:
            tube = you.split('$')
            if tube[0] == mainYoutube:
                youtube_main = tube[1]
            saveYoutube.append(tube[1])
    sYoutube = "|".join(saveYoutube)


    # 기타
    etcSaveCareer = request.POST.get('etcSaveCareer')
    saveForeign = request.POST['saveForeign']
    saveSpecialty = request.POST['saveSpecialty']
    introduction = request.POST['introduction']
    notView = request.POST.get('notView', "0")
    delCareer = request.POST.get("delCareer", "")
    etcDelCareer = request.POST.get("etcDelCareer", "")

    print(notView)

    profiles = ProfileInfo.objects.get(num=num)

    nowTime = timezone.now()

    # 메인 이미지 등록
    if len(mainImage) > 0 :
        # 기존 이미지 삭제
        for rmImages in mainImg:
            if (rmImages == ""): continue
            deleteFile(rmImages)

        for image in mainImage:
            sub = image.name.split('.')[-1]
            url = uploadFile(image, "photos/profiles/main/", sub)  # 파일 업로드
            image_main = url

    else :
        image_main = mainImg


    # 프로필 이미지 처리
    if profiles.detailimage != None :
        profileImgArr = profiles.detailimage.split("|")
    else :
        profileImgArr = []
    rmImage = removeImage_detail.split('|')
    if (removeImage_detail != ""):
        for rmImages in rmImage:
            if (rmImages == ""): continue
            deleteFile(rmImages)
            profileImgArr.remove(rmImages)

    addImage = []
    if len(profileImage) != 0:
        count = 0
        for image in profileImage:
            count = count + 1
            sub = image.name.split('.')[-1]
            url = uploadFile(image, "photos/profile/additional/", sub)  # 파일 업로드
            addImage.append(url)

    if len(profileImgArr) > 0 :
        profileDetail_image = profileImgArr + addImage
    else :
        profileDetail_image = addImage

    proDetail = "|".join(profileDetail_image)

    # 작품 이미지 등록
    if profiles.artimage != None :
        actImageArr = profiles.artimage.split("|")
    else :
        actImageArr = []

    rmImage = removeImage_art.split('|')
    if (removeImage_art != ""):
        for rmImages in rmImage:
            if (rmImages == ""): continue
            deleteFile(rmImages)
            actImageArr.remove(rmImages)

    addImage = []
    if len(userImage) != 0:
        count = 0
        for image in profileImage:
            count = count + 1
            sub = image.name.split('.')[-1]
            url = uploadFile(image, "photos/profile/additional/", sub)  # 파일 업로드
            addImage.append(url)

    artImageDetail = actImageArr + addImage
    artImage = "|".join(artImageDetail)

    # 기본정보 수정.
    userInfo = UserInfo.objects.get(userid=userID)
    userInfo.nationality = nationality;
    userInfo.military = military;
    userInfo.entertain = entertain;
    userInfo.finalschool = finalSchool;
    userInfo.school = school;
    userInfo.major = major;
    userInfo.instargram = instagram;
    userInfo.youtube = youtube;
    userInfo.save();

    profiles.profileimage = image_main
    profiles.detailimage =proDetail
    profiles.artimage =artImage
    profiles.height=height
    profiles.weight=weight
    profiles.topsize=topSize
    profiles.bottomsize=bottomSize
    profiles.shoessize=shoesSize
    profiles.skincolor=skinColor
    profiles.haircolor=hairColor
    profiles.foreign=saveForeign
    profiles.mainyoutube=youtube_main
    profiles.youtube=sYoutube
    profiles.talent=saveSpecialty
    profiles.comment=introduction
    profiles.intercate=cate_m
    profiles.intersubcate=cate_s
    profiles.iscareer=notCareer
    profiles.careeryear=allCareer_y
    profiles.careermonth=allCareer_m
    profiles.public=notView
    profiles.contenttype=""
    profiles.update=nowTime
    profiles.save()


    if notCareer == "0":
        career = saveCareer.split('|')
        for careers in career:
            # c_cateM_val + "$" + c_cateM + "$" + c_cateS_val + "$" + c_cateS + "$" + c_title + "$" + c_role
            careerContent = careers.split('$')

            getCareer = ProfileCareer.objects.filter( profilenum=num, catetype=careerContent[0],
                                                         catesubtype=careerContent[2],
                                                         title=careerContent[4], role=careerContent[5] )

            if getCareer.count() == 0 :
                saveProCareer = ProfileCareer.objects.create(userid=userID, profilenum=num, catetype=careerContent[0],
                                                             catesubtype=careerContent[2],
                                                             title=careerContent[4], role=careerContent[5], regtime=nowTime)

    else :
        getCareer = ProfileCareer.objects.filter(profilenum=num)
        getCareer.delete() # 경력없음일경우 모두 삭제.

    if delCareer != "" :
        delCareers = delCareer.split('|')
        for careers in delCareers :
            careerContent = careers.split('$')
            getCareer = ProfileCareer.objects.filter(profilenum=num, catetype=careerContent[0],
                                                     catesubtype=careerContent[2],
                                                     title=careerContent[4], role=careerContent[5])
            getCareer.delete()


    if etcSaveCareer != "":
        etcCareer = etcSaveCareer.split('|')
        for careers in etcCareer:
            # ec_cateM + "$" + ec_cateS + "$" + ec_title + "$" + ec_role;
            careerContent = careers.split('$')

            getEtcCareer = ProfileEtccareer.objects.filter( profilenum=num, catetype=careerContent[0],
                                                               subcatetype=careerContent[1],
                                                               title=careerContent[2], role=careerContent[3] )

            if getEtcCareer.count() == 0 :
                saveProCareerEtc = ProfileEtccareer.objects.create(userid=userID, profilenum=num, catetype=careerContent[0],
                                                                   subcatetype=careerContent[1],
                                                                   title=careerContent[2], role=careerContent[3],
                                                                   regtime=nowTime)
    # 기타 경력 삭제
    if etcDelCareer != "" :
        etcCareer = etcDelCareer.split('|')
        for careers in etcCareer:
            # ec_cateM + "$" + ec_cateS + "$" + ec_title + "$" + ec_role;
            careerContent = careers.split('$')

            getEtcCareer = ProfileEtccareer.objects.filter( profilenum=num, catetype=careerContent[0],
                                                               subcatetype=careerContent[1],
                                                               title=careerContent[2], role=careerContent[3] )
            getEtcCareer.delete()


    return redirect('/profile/profileDetail/all/' + num + "/")


def pofile_delete(request, num) :

    profiles = ProfileInfo.objects.get(num=num)
    profiles.isdelete = '1'
    profiles.save()

    return redirect("/")

def audiAjaxGetCate(request) :

    cate = request.GET.get('cate')
    catesub = CateSub.objects.filter(catecode=cate).order_by("cateorder")

    return render(request, 'profiles/ajax_cate.html', {'catesub':catesub})


def audiAjaxGetCateEtc(request) :

    cate = request.GET.get('cate')

    return render(request, 'profiles/ajax_cate_etc.html', {'cate':cate})

def getProfile(request) :

    order = request.GET['order']
    nationality = request.GET['nationality']
    geneder = request.GET['geneder']
    military = request.GET['military']
    foreign = request.GET['foreign']
    good = request.GET['good']
    age1 = request.GET['age1']
    age2 = request.GET['age2']
    school = request.GET['school']
    height1 = request.GET['height1']
    height2 = request.GET['height2']
    career1 = request.GET['career1']
    page = request.GET['page']
    cate_type = request.GET['cate_type']

    orderby = ""
    if order == "popular":
        orderby = " order by viewCount desc "
    elif order == "recommend":
        orderby = " order by pickCount desc "
    else:
        orderby = " order by `upDate` Desc, regDate DESC "

    where = ""
    if nationality != "" :
        where = where + " and nationality='"+ nationality + "'"

    if military != "" :
        where = where + " and military='"+ military + "'"

    if geneder != "" :
        where = where + " and gender='"+ geneder + "'"

    if foreign != "" :
        if good != "":
            where = where + " and `foreign` like '%" + foreign+"$" + good + "%'"
        else :
            where = where + " and `foreign` like '%" + foreign + "%'"

    if age1 != "" and age2 != "" :
        nowTime = str(timezone.now())
        year = nowTime.split('-')

        age_1 = int(year[0]) - int(age1) + 1
        age_2 = int(year[0]) - int(age2) + 1

        where = where + " and birth >= '"+ str(age_1) + "-01-01' and birth <= '"+ str(age_2) + "-12-31' "

    if school != "":
        where = where + " and school like '%" + school + "%'"

    if height1 != "" and height2 != "" :
        where = where + " and height >= '"+ height1 + "' and height <= '"+ height2 + "' "

    if career1 != "" :
        where = where + " and careerYear >= '"+ career1 +"' "

    if cate_type == "actor":
        where = where + "and ( p.interCate = 'mainCate1' || p.interCate like '%배우%' ) "
    elif cate_type == "model":
        where = where + "and ( p.interCate = 'mainCate2' || p.interCate like '%모델%' ) "
    elif cate_type == "singer":
        where = where + "and ( p.interCate = 'mainCate3' || p.interCate like '%가수%' ) "

    try:
        cursor = connection.cursor()
        user = request.session.get('id', '')

        block = 10
        start = (int(page) - 1) * block
        end = int(page) * block

        # 프로필
        if user:
            query = "SELECT p.num , profileImage, height, weight, viewCount, pickCount, cViewCount, ui.name, ui.birth, ui.entertain, " \
                    "       ui.gender, ui.military, ui.school, ui.major, talent, comment, mainYoutube, isCareer, (SELECT COUNT(*) FROM profile_pick WHERE userID = '" + user + "' AND profileNum = p.num ) AS proPick " \
                    "FROM profile_info AS p LEFT JOIN user_info AS ui  ON p.userID = ui.userID " \
                    "WHERE public = '0' and isDelete = '0'  and ui.userID != '' " + where + orderby + " LIMIT " + str(start) + ", " + str(block)
        else:
            query = "SELECT p.num, profileImage, height, weight, viewCount, pickCount, cViewCount, ui.name, ui.birth, ui.entertain," \
                    "       ui.gender, ui.military, ui.school, ui.major, talent, comment, mainYoutube, isCareer, '0' AS proPick " \
                    "FROM profile_info AS p LEFT JOIN user_info AS ui " \
                    "     ON p.userID = ui.userID " \
                    "WHERE public = '0' and isDelete = '0'  and ui.userID != '' " + where + orderby + " LIMIT " + str(start) + ", " + str(block)

        result = cursor.execute(query)
        profiles = cursor.fetchall()

        connection.commit()
        connection.close()

    except:
        connection.rollback()

    return render(request, 'profiles/ajax_profileList.html', {'profiles':profiles})


def getCareerList(profileNum, groupType) :

    try:
        cursor = connection.cursor()

        query = "SELECT profileNum, title, ROLE, cm.cateName AS mainCate, cs.cateName AS subCate  " \
                "FROM profile_career AS pc LEFT JOIN cate_main AS cm ON pc.cateType = cm.cateCode " \
                "     LEFT JOIN cate_sub AS cs ON pc.cateSubType = cs.subCate " \
                "WHERE pc.profileNum = '"+ str(profileNum) +"' AND cs.otherGroup = '"+groupType+"'"

        result = cursor.execute(query)
        cateList = cursor.fetchall()

        connection.commit()
        connection.close()

    except:
        connection.rollback()

    return cateList

def saveComment(request) :

    comment = request.GET['comment']
    num = request.GET['num']
    userID = request.session['id']

    nowTime = timezone.now()

    save = ProfileComment.objects.create(profilenum=num,userid=userID,content=comment,regtime=nowTime)

    return JsonResponse({"code": "0"})

def reloadComment(request) :
    num = request.GET['num']

    comment = ProfileComment.objects.filter(profilenum=num).order_by("-num")

    return render(request, 'profiles/ajax_comment.html', {'comment': comment})

def deleteComment(request) :

    num = request.GET['num']

    comment = ProfileComment.objects.get(num=num)
    comment.delete()

    return JsonResponse({"code": "0"})

def profileSuggest(request) :

    audiNum = request.GET['audiNum']
    comment = request.GET['comment']
    num = request.GET['num']
    writeUID = request.GET['writeUID']
    userID = request.GET['userID']

    nowTime = timezone.now()

    saveSuggest = ProfileSuggest.objects.create(userid=writeUID, suuserid=userID, profilenum=num, auditionnum=audiNum,
                                                comment=comment, regtime=nowTime)

    writer = UserInfo.objects.get(userid=writeUID)
    sender = UserCompany.objects.get(userid=userID)

    sendSMS(writer.phone, "오디션 제안", "[ONEPICK] " +sender.name + "에서 오디션 제안이 도착했습니다." )

    return JsonResponse({"code": "0"})


def printProfile(request, type, num) :

    profile = ProfileInfo.objects.get(num=num)
    userInfo = UserInfo.objects.get(userid=profile.userid)

    career = ProfileCareer.objects.filter(profilenum=num)
    movieCareer = getCareerList(num, "movie")
    dramaCareer = getCareerList(num, "drama")
    etcCareer = getCareerList(num, "etc")

    if (profile.detailimage):
        profileImages = profile.detailimage.split("|")
    else:
        profileImages = ""

    return render(request, 'profiles/profile_width.html', {'profile': profile, 'userInfo': userInfo, 'career':career,
                                                           'movieCareer':movieCareer, 'dramaCareer':dramaCareer, 'etcCareer':etcCareer,
                                                           'profileImages':profileImages })