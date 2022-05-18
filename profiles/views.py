from django.shortcuts import render, redirect
from picktalk.models import *
import boto3
import datetime
from django.utils import timezone
from django.conf import settings
import hashlib
from audition.views import md5_generator


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

def listView(request, cate_type, orderby): # 오디션 Main

    """
    order = orderbyType(orderby)
    cate = getCateType(cate_type)
    profileList = ProfileInfo.objects.filter(careers__applySubType__applyType_id=cate).distinct().order_by(order)[:12]

    return render(request, 'profiles/list.html', {'cateType' : cate_type, "profileList" : profileList } )

    """
    return render(request, 'profiles/list.html')


def viewer(request, cate_type, num) :

    """
    profileData = ProfileInfo.objects.filter(id=num)

    for row in profileData.values_list():
        userID = row[1]
        youtube = row[10]

    youtube = youtube.replace("https://youtu.be/", "https://www.youtube.com/embed/")

    userData = UserInfo.objects.filter(id=userID)

    cate = CateMain.objects.filter(applysubtype__career__profile_id=num).distinct()

    return render(request, 'profiles/viewer.html', { 'cateType' : cate_type , "num":num, "profileData" : profileData,
                                                     "userData" : userData, "youtube" : youtube, "cate" : cate })
    """

    return render(request, 'profiles/viewer.html')

def viewerDetail(request, type, num) :

    """
    if type == "youtube" :
        profileData = ProfileInfo.objects.filter(id=num)

        for row in profileData.values_list():
            data = row[10].replace("https://youtu.be/", "https://www.youtube.com/embed/")

    elif type == "image" :
        data = ProfileImage.objects.filter(profile__id=num)
        print(data)

    elif type == "career" :
        data = AuditionSubCategory.objects.filter(applysubtype__career__profile_id=num).values('name', 'applysubtype__career__contents')
        #print(str(data.query))
        #print(data)
        #for row in data.values_list():
        #    print(row)


    return render(request, 'profiles/viewer_detail.html', { 'type' :  type , 'num' : num, 'data' : data })
    """
    return render(request, 'profiles/viewer_detail.html')



def pofile_write(request) :

    userID = request.session['id']
    user = UserInfo.objects.get(userid=userID)
    cate = CateMain.objects.all()

    return render(request, 'profiles/write.html', { 'user':user, 'cate' : cate })

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

    print(notCareer + " " + saveCareer)

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
                                             regdate=nowTime, viewcount=0, cviewcount=0, public=notView,isdelete=0 )

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



def audiAjaxGetCate(request) :

    cate = request.GET.get('cate')
    catesub = CateSub.objects.filter(catecode=cate).order_by("cateorder")

    return render(request, 'profiles/ajax_cate.html', {'catesub':catesub})


def audiAjaxGetCateEtc(request) :

    cate = request.GET.get('cate')

    return render(request, 'profiles/ajax_cate_etc.html', {'cate':cate})

