from django.shortcuts import render, redirect
from picktalk.models import *
import boto3
import datetime
from django.utils import timezone
from django.conf import settings
import hashlib
from audition.views import md5_generator
from django.http import HttpResponse, JsonResponse
from django.db import connection


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


def listView(request, cate_type): # 오디션 Main

    try:
        cursor = connection.cursor()

        user = request.session.get('id', '')

        # 프로필
        if user:
            query = "SELECT p.num , profileImage, height, weight, viewCount, pickCount, cViewCount, ui.name, ui.birth, ui.entertain, " \
                    "       ui.gender, ui.military, ui.school, ui.major, talent, comment, mainYoutube, isCareer, (SELECT COUNT(*) FROM profile_pick WHERE userID = '" + user + "' AND profileNum = p.num ) AS proPick " \
                    "FROM profile_info AS p LEFT JOIN user_info AS ui  ON p.userID = ui.userID " \
                    "WHERE public = '0' and isDelete = '0' " \
                    "ORDER BY regDate DESC " \
                    "LIMIT 15"
        else:
            query = "SELECT p.num, profileImage, height, weight, viewCount, pickCount, cViewCount, ui.name, ui.birth, ui.entertain," \
                    "       ui.gender, ui.military, ui.school, ui.major, talent, comment, mainYoutube, isCareer, '0' AS proPick " \
                    "FROM profile_info AS p LEFT JOIN user_info AS ui " \
                    "     ON p.userID = ui.userID " \
                    "WHERE public = '0' and isDelete = '0' " \
                    "ORDER BY regDate DESC  " \
                    "LIMIT 15"

        result = cursor.execute(query)
        profiles = cursor.fetchall()

        connection.commit()
        connection.close()

    except:
        connection.rollback()
    return render(request, 'profiles/list.html', { 'profiles':profiles, "cateType" : cate_type })


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
        pick = ProfilePick.objects.filter(userid=user)
        if pick.count() == 0 :
            pickCheck = "0"
        else :
            pickCheck = "1"

    else :
        pickCheck = "0"

    profileImages = profiles.detailimage.split("|")
    artImages = profiles.artimage.split("|")
    youtubes = profiles.youtube.split("|")
    foreign = profiles.foreign.split("|")
    talent = profiles.talent.split("|")

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

    profileImages = profiles.detailimage.split("|")
    artImages = profiles.artimage.split("|")
    youtubes = profiles.youtube.split("|")
    foreign = profiles.foreign.split("|")
    talent = profiles.talent.split("|")

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

    # 이미지 등록
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )

    nowTime = timezone.now()

    # 메인 이미지 등록
    for image in mainImage :
        sub = image.name.split('.')[-1]
        imgName = userID + "_userMain_" + str(nowTime)
        imageName = md5_generator(imgName) + "." + sub

        s3_client.upload_fileobj(
            image,
            settings.AWS_STORAGE_BUCKET_NAME,
            "media/photos/profiles/main/" + imageName,
            ExtraArgs={
                "ContentType": image.content_type,
            }
        )
        image_main = "photos/profiles/main/" + imageName

    # 프로필 이미지 등록.
    image_profile = ""
    if len(profileImage) != 0 :
        count = 0
        for image in profileImage:
            count = count + 1
            sub = image.name.split('.')[-1]
            imgName = userID + "_profile_" + str(count) + "_" + str(nowTime)
            imageName = md5_generator(imgName) + "." + sub

            s3_client.upload_fileobj(
                image,
                settings.AWS_STORAGE_BUCKET_NAME,
                "media/photos/profile/additional/" + imageName,
                ExtraArgs={
                    "ContentType": image.content_type,
                }
            )
            if (count == 1):
                image_profile = "photos/profile/additional/" + imageName
            else:
                image_profile = image_profile + "|" + "photos/profile/additional/" + imageName

    image_act = ""
    if len(userImage) != 0 :
        count = 0
        for image in userImage:
            count = count + 1
            sub = image.name.split('.')[-1]
            imgName = userID + "_actImage_" + str(count)  + "_" + str(nowTime)
            imageName = md5_generator(imgName) + "." + sub

            s3_client.upload_fileobj(
                image,
                settings.AWS_STORAGE_BUCKET_NAME,
                "media/photos/profile/additional/" + imageName,
                ExtraArgs={
                    "ContentType": image.content_type,
                }
            )
            if (count == 1):
                image_act = "photos/profile/additional/" + imageName
            else:
                image_act = image_act + "|" + "photos/profile/additional/" + imageName




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
    user = UserInfo.objects.get(userid=userID)
    cate = CateMain.objects.all()
    profiles = ProfileInfo.objects.get(num=num)
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

    profileImages = profiles.detailimage.split("|")
    artImages = profiles.artimage.split("|")
    youtubes = profiles.youtube.split("|")
    foreign = profiles.foreign.split("|")
    talent = profiles.talent.split("|")
    careerEtc = ProfileEtccareer.objects.filter(profilenum=num).order_by("num")

    return render(request, 'profiles/edit.html', { 'user':user, 'cate' : cate, 'num' : num, 'profiles' : profiles,
                                                   'catesub':catesub, "careerList" : careerList, "profileImages" : profileImages,
                                                   "artImages":artImages, "youtubes":youtubes, "foreign": foreign, "talent": talent,
                                                   "careerEtc":careerEtc})


def pofile_edit_callback(request) :
    # 기본정보
    num = request.POST['num']
    userID = request.POST['userID']
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


    profiles = ProfileInfo.objects.get(num=num)


    # 이미지 등록
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )

    s3 = boto3.resource('s3',
                        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                        )

    nowTime = timezone.now()

    # 메인 이미지 등록
    if len(mainImage) > 0 :
        # 기존 이미지 삭제
        for rmImages in mainImg:
            if (rmImages == ""): continue
            img = rmImages.replace("photos/profiles/main/", "")
            s3.Object(settings.AWS_STORAGE_BUCKET_NAME, "media/photos/profiles/main/" + img).delete()
        
        #신규 이미지 업데이트
        for image in mainImage:
            sub = image.name.split('.')[-1]
            imgName = userID + "_userMain_" + str(nowTime)
            imageName = md5_generator(imgName) + "." + sub

            s3_client.upload_fileobj(
                image,
                settings.AWS_STORAGE_BUCKET_NAME,
                "media/photos/profiles/main/" + imageName,
                ExtraArgs={
                    "ContentType": image.content_type,
                }
            )
            image_main = "photos/profiles/main/" + imageName

    else :
        image_main = mainImg


    # 프로필 이미지 처리
    profileImgArr = profiles.detailimage.split("|")
    rmImage = removeImage_detail.split('|')
    if (removeImage_detail != ""):
        s3 = boto3.resource('s3',
                            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                            )

        for rmImages in rmImage:
            if (rmImages == ""): continue
            img = rmImages.replace("photos/profile/additional/", "")
            s3.Object(settings.AWS_STORAGE_BUCKET_NAME, "media/photos/profile/additional/" + img).delete()
            profileImgArr.remove(rmImages)

    addImage = []
    if len(profileImage) != 0:
        count = 0
        for image in profileImage:
            count = count + 1
            sub = image.name.split('.')[-1]
            imgName = userID + "_profile_" + str(count) + "_" + str(nowTime)
            imageName = md5_generator(imgName) + "." + sub

            s3_client.upload_fileobj(
                image,
                settings.AWS_STORAGE_BUCKET_NAME,
                "media/photos/profile/additional/" + imageName,
                ExtraArgs={
                    "ContentType": image.content_type,
                }
            )

            addImage.append("photos/profile/additional/" + imageName)

    profileDetail_image =  profileImgArr + addImage
    proDetail = "|".join(profileDetail_image)

    # 작품 이미지 등록
    actImageArr = profiles.artimage.split("|")
    rmImage = removeImage_art.split('|')
    if (removeImage_art != ""):
        s3 = boto3.resource('s3',
                            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                            )

        for rmImages in rmImage:
            if (rmImages == ""): continue
            img = rmImages.replace("photos/profile/additional/", "")
            s3.Object(settings.AWS_STORAGE_BUCKET_NAME, "media/photos/profile/additional/" + img).delete()
            actImageArr.remove(rmImages)

    addImage = []
    if len(userImage) != 0:
        count = 0
        for image in userImage:
            count = count + 1
            sub = image.name.split('.')[-1]
            imgName = userID + "_userImage_" + str(count) + "_" + str(nowTime)
            imageName = md5_generator(imgName) + "." + sub

            s3_client.upload_fileobj(
                image,
                settings.AWS_STORAGE_BUCKET_NAME,
                "media/photos/profile/additional/" + imageName,
                ExtraArgs={
                    "ContentType": image.content_type,
                }
            )

            addImage.append("photos/profile/additional/" + imageName)

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

    order = request.POST['order']
    nationality = request.POST['nationality']
    geneder = request.POST['geneder']
    military = request.POST['military']
    foreign = request.POST['foreign']
    good = request.POST['good']
    age1 = request.POST['age1']
    age2 = request.POST['age2']
    school = request.POST['school']
    height1 = request.POST['height1']
    height2 = request.POST['height2']
    career1 = request.POST['career1']
    career2 = request.POST['career2']

    orderby = ""
    if order == "popular":
        orderby = " order by viewCount desc "
    elif order == "recommend":
        orderby = " order by pickCount desc "
    else:
        orderby = " order by regDate desc "

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

    if career1 != "" and career2 != "" :
        where = where + " and careerYear >= '"+ career1 + "' and careerYear <= '"+ career2 + "' "

    try:
        cursor = connection.cursor()
        user = request.session.get('id', '')

        # 프로필
        if user:
            query = "SELECT p.num , profileImage, height, weight, viewCount, pickCount, cViewCount, ui.name, ui.birth, ui.entertain, " \
                    "       ui.gender, ui.military, ui.school, ui.major, talent, comment, mainYoutube, isCareer, (SELECT COUNT(*) FROM profile_pick WHERE userID = '" + user + "' AND profileNum = p.num ) AS proPick " \
                    "FROM profile_info AS p LEFT JOIN user_info AS ui  ON p.userID = ui.userID " \
                    "WHERE public = '0' and isDelete = '0' " + where + orderby + " LIMIT 15"
        else:
            query = "SELECT p.num, profileImage, height, weight, viewCount, pickCount, cViewCount, ui.name, ui.birth, ui.entertain," \
                    "       ui.gender, ui.military, ui.school, ui.major, talent, comment, mainYoutube, isCareer, '0' AS proPick " \
                    "FROM profile_info AS p LEFT JOIN user_info AS ui " \
                    "     ON p.userID = ui.userID " \
                    "WHERE public = '0' and isDelete = '0' " + where + orderby + " LIMIT 15"

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

    return JsonResponse({"code": "0"})


def printProfile(request, type, num) :


    return render(request, 'profiles/profile_width.html' )