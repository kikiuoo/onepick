from django.shortcuts import render
from picktalk.models import *



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



def audiAjaxGetCate(request) :

    cate = request.GET.get('cate')
    catesub = CateSub.objects.filter(catecode=cate).order_by("cateorder")

    return render(request, 'profiles/ajax_cate.html', {'catesub':catesub})


def audiAjaxGetCateEtc(request) :

    cate = request.GET.get('cate')

    return render(request, 'profiles/ajax_cate_etc.html', {'cate':cate})

