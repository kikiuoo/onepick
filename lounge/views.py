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

def main(request):

    qaList = QaNotice.objects.filter(viewtype="Y").order_by("-regdate")[:1]
    magaList = BoradMagazine.objects.all().order_by("-regdate")[:5]
    bullList = BoradBulletin.objects.all().order_by("-regdate")[:5]

    cursor = connection.cursor()

    query = "SELECT qq.num, cateName, title, regDate, IFNULL(commCnt, 0) AS commCnt, secret, qq.userID " \
            "FROM qa_qanda AS qq LEFT JOIN qa_qanda_cate AS qqc  ON qq.cate = qqc.cateCode " \
            "     LEFT JOIN ( SELECT COUNT(*) AS commCnt, qaNum FROM qa_qanda_comment GROUP BY qaNum ) AS qqc ON qq.num = qqc.qaNum " \
            "order by qq.regDate desc limit 5 "

    result = cursor.execute(query)
    qandaList = cursor.fetchall()

    connection.commit()
    connection.close()

    return render(request, 'lounge/main.html',
                  {"qaList" : qaList, "magaList" : magaList, "qandaList" : qandaList, "bullList" : bullList})




def notice(request, num) :
    notice = QaNotice.objects.get(num=num)

    image = ""
    if notice.image != "" and notice.image != None :
        image = notice.image.split("|")

    notice.viewcount = notice.viewcount + 1
    notice.save()

    nowTime = timezone.now()
    user = request.session.get('id', '')
    saveNoticeView = QaNoticeView.objects.create(noticenum=num, userid=user, regtime=nowTime)

    return render(request, 'lounge/notice.html', {"notice": notice, "image" : image})


def notiList(request, page) :

    block = 10
    start = (page - 1) * block
    end = page * block

    noti = QaNotice.objects.filter(viewtype="Y")
    notice = noti.order_by("-regdate")[start:end]

    allPage = ( noti.count() / block ) + 1

    paging = getPageList( page, allPage )

    return render(request, 'lounge/notiList.html', {"notice": notice, "paging" : paging, "page":page})



def qandaList(request, page) :

    block = 10
    start = (page - 1) * block
    end = page * block

    cursor = connection.cursor()

    query = "SELECT qq.num, cateName, title, regDate, IFNULL(commCnt, 0) AS commCnt, secret, qq.userID  " \
            "FROM qa_qanda AS qq LEFT JOIN qa_qanda_cate AS qqc  ON qq.cate = qqc.cateCode " \
            "     LEFT JOIN ( SELECT COUNT(*) AS commCnt, qaNum FROM qa_qanda_comment GROUP BY qaNum ) AS qqc ON qq.num = qqc.qaNum " \
            "order by qq.regDate desc limit " + str(start) + ", " + str(block)

    result = cursor.execute(query)
    qandaList = cursor.fetchall()

    connection.commit()
    connection.close()

    allPage = (len(qandaList) / block) + 1

    paging = getPageList(page, allPage)

    return render(request, 'lounge/qandaList.html', {"qandaList": qandaList, "paging" : paging, "page":page,"type": "list"})



def qandaMyList(request, page) :

    block = 10
    start = (page - 1) * block
    end = page * block

    cursor = connection.cursor()

    user = request.session.get('id', '')

    query = "SELECT qq.num, cateName, title, regDate, IFNULL(commCnt, 0) AS commCnt, secret, qq.userID " \
            "FROM qa_qanda AS qq LEFT JOIN qa_qanda_cate AS qqc  ON qq.cate = qqc.cateCode " \
            "     LEFT JOIN ( SELECT COUNT(*) AS commCnt, qaNum FROM qa_qanda_comment GROUP BY qaNum ) AS qqc ON qq.num = qqc.qaNum " \
            "where qq.userID = '"+user+"' " \
            "order by qq.regDate desc limit " + str(start) + ", " + str(block)

    result = cursor.execute(query)
    qandaList = cursor.fetchall()

    connection.commit()
    connection.close()

    allPage = (len(qandaList) / block) + 1

    paging = getPageList(page, allPage)

    return render(request, 'lounge/qandaList.html', {"qandaList": qandaList, "paging" : paging, "page":page,"type": "myList"})


def qandaWrite(request) :

    cates = QaQandaCate.objects.all()

    return render(request, 'lounge/qandaWrite.html', {"cates": cates})

def qandaWriteCallBack(request) :

    cate = request.POST['cate']
    title = request.POST['title']
    content = request.POST['content']
    secret = request.POST.get('secret', "N")

    user = request.session.get('id', '')

    nowTime = timezone.now()

    saveQaQanda = QaQanda.objects.create(userid=user, cate=cate, title=title, content=content, regdate=nowTime, secret=secret, viewcount=0)

    return redirect("/lounge/qanda/list/1/")


def qandaEdit(request, num) :

    qanda = QaQanda.objects.get(num=num)
    cates = QaQandaCate.objects.all()

    return render(request, 'lounge/qandaEdit.html', {"qanda":qanda, "cates": cates} )

def qandaEditCallBack(request) :

    num = request.POST['num']
    cate = request.POST['cate']
    title = request.POST['title']
    content = request.POST['content']
    secret = request.POST.get('secret', "N")

    qanda = QaQanda.objects.get(num=num)
    qanda.title = title
    qanda.cate = cate
    qanda.content = content
    qanda.secret = secret
    qanda.save()

    return redirect("/lounge/qanda/viewer/"+num+"/")


def qandaDelete(request, num) :

    qanda = QaQanda.objects.get(num=num)
    qanda.delete()

    return redirect("/lounge/qanda/list/1/")


def qandaView(request, num) :

    qanda = QaQanda.objects.get(num=num)
    cate = QaQandaCate.objects.get(catecode=qanda.cate)
    user = UserInfo.objects.filter(userid=qanda.userid)

    comment = QaQandaComment.objects.filter(qanum=num).order_by("-num")

    qanda.viewcount = qanda.viewcount + 1
    qanda.save()

    nowTime = timezone.now()
    users = request.session.get('id', '')
    saveNoticeView = QaQandaView.objects.create(qanum=num, userid=users, regtime=nowTime)

    return render(request, 'lounge/qandaView.html', {"qanda": qanda, "cate" : cate, "user" : user,
                                                       "comment" : comment})


def qaSaveComment(request) :

    comment = request.GET['comment']
    num = request.GET['num']
    userID = request.session['id']

    nowTime = timezone.now()

    print(num)

    save = QaQandaComment.objects.create(qanum=str(num),userid=userID,content=comment,regtime=nowTime)

    return JsonResponse({"code": "0"})


def qaReloadComment(request) :
    num = request.GET['num']

    comment = QaQandaComment.objects.filter(qanum=num).order_by("-num")

    return render(request, 'picktalk/ajax_comment.html', {'comment': comment})

def qaDeleteComment(request) :

    num = request.GET['num']

    comment = QaQandaComment.objects.get(num=num)
    comment.delete()

    return JsonResponse({"code": "0"})







def magaList(request, page) :

    block = 10
    start = (page - 1) * block
    end = page * block

    magaAll = BoradMagazine.objects.all()
    magazine = magaAll.order_by("-regdate")[start:end]

    allPage = ( magaAll.count() / block ) + 1

    paging = getPageList(page, allPage)

    return render(request, 'lounge/magaList.html', {"magazine": magazine, "paging" : paging, "page":page})

def magaView(request, num) :

    magazine = BoradMagazine.objects.get(num=num)

    if magazine.image :
        images = magazine.image.split("|")
    else :
        images = ""

    comment = BoardMagazineComment.objects.filter(mgnum=num).order_by("-num")

    magazine.viewcount = magazine.viewcount + 1
    magazine.save()

    nowTime = timezone.now()
    users = request.session.get('id', '')
    saveView = BoradMagazineView.objects.create(maganum=num, userid=users, regtime=nowTime)

    return render(request, 'lounge/magaView.html', {"magazine": magazine, "image" : images, "comment" : comment})

def magaWrite(request) :

    return render(request, 'lounge/magaWrite.html')

def magaWriteCallBack(request) :

    title = request.POST['title']
    content = request.POST['content']

    userImage = request.FILES.getlist('userImage[]')

    nowTime = timezone.now()
    imageURL = ""
    count = 0
    for image in userImage:
        count = count + 1
        sub = image.name.split('.')[-1]
        url = uploadFile(image, "photos/magazine/image", sub)

        if (count == 1):
            imageURL = url
        else:
            imageURL = imageURL + "|" + url


    user = request.session.get('id', '')

    saveQaQanda = BoradMagazine.objects.create(userid=user, title=title, content=content, image=imageURL, regdate=nowTime, viewcount=0)

    return redirect("/lounge/magazine/list/1/")


def magaEdit(request, num) :

    magazine = BoradMagazine.objects.get(num=num)

    image = magazine.image.split('|')

    return render(request, 'lounge/magaEdit.html', {"magazine":magazine, "image" : image})

def magaEditCallBack(request) :

    num = request.POST['num']
    title = request.POST['title']
    content = request.POST['content']

    removeImage = request.POST.get('removeImage', "")

    userImage = request.FILES.getlist('userImage[]')

    # 이미지 등록.
    nowTime = timezone.now()

    addImage = []
    for image in userImage:
        sub = image.name.split('.')[-1]
        url = uploadFile(image, "photos/audition/image", sub)  # 파일 업로드

        addImage.append(url)

    # DB에서 이미지 저장된 내용 빼기.
    magazine = BoradMagazine.objects.get(num=num)
    dbImage = magazine.image.split('|')

    # 이미지 삭제.
    rmImage = removeImage.split('|')
    if (removeImage != ""):
        for rmImages in rmImage:
            if (rmImages == ""): continue
            deleteFile(rmImages)
            dbImage.remove(rmImages)

    saveImage = dbImage + addImage
    imageUrl = "|".join(saveImage)



    magazine.title = title
    magazine.content = content
    magazine.image = imageUrl
    magazine.save()

    return redirect("/lounge/magazine/viewer/"+num+"/")


def magaDelete(request, num) :

    magazine = BoradMagazine.objects.get(num=num)

    # 이미지 삭제.
    rmImage = magazine.image.split('|')
    for rmImages in rmImage:
        if (rmImages == ""): continue
        deleteFile(rmImages)

    magazine.delete()

    return redirect("/lounge/magazine/list/1/")


def magaSaveComment(request) :

    comment = request.GET['comment']
    num = request.GET['num']
    userID = request.session['id']

    nowTime = timezone.now()

    print(num)

    save = BoardMagazineComment.objects.create(mgnum=str(num),userid=userID,content=comment,regtime=nowTime)

    return JsonResponse({"code": "0"})


def magaReloadComment(request) :
    num = request.GET['num']

    comment = BoardMagazineComment.objects.filter(mgnum=num).order_by("-num")

    return render(request, 'picktalk/ajax_comment.html', {'comment': comment})

def magaDeleteComment(request) :

    num = request.GET['num']

    comment = BoardMagazineComment.objects.get(num=num)
    comment.delete()

    return JsonResponse({"code": "0"})









def bullList(request, page) :

    block = 10
    start = (page - 1) * block
    end = page * block

    bullAll = BoradBulletin.objects.all()
    bulletin = bullAll.order_by("-regdate")[start:end]

    allPage = ( bullAll.count() / block ) + 1

    paging = getPageList(page, allPage)

    return render(request, 'lounge/bullList.html', {"bulletin": bulletin, "paging" : paging, "page":page})

def bullView(request, num) :

    bull = BoradBulletin.objects.get(num=num)
    user = UserInfo.objects.filter(userid=bull.userid)

    comment = BoradBulletinComment.objects.filter(bulnum=num).order_by("-num")


    bull.viewcount = bull.viewcount + 1
    bull.save()

    nowTime = timezone.now()
    users = request.session.get('id', '')
    saveView = BoradBulletinView.objects.create(bullnum=num, userid=users, regtime=nowTime)

    return render(request, 'lounge/bullView.html', {"bull": bull, "user" : user, "comment" : comment})

def bullWrite(request) :

    return render(request, 'lounge/bullWrite.html')

def bullWriteCallBack(request) :

    title = request.POST['title']
    content = request.POST['content']

    user = request.session.get('id', '')

    nowTime = timezone.now()

    saveQaQanda = BoradBulletin.objects.create(userid=user, title=title, content=content, regdate=nowTime, viewcount=0)

    return redirect("/lounge/bull/list/1/")




def bullEdit(request, num) :

    bull = BoradBulletin.objects.get(num=num)

    return render(request, 'lounge/bullEdit.html', {"bull":bull} )

def bullEditCallBack(request) :

    num = request.POST['num']
    title = request.POST['title']
    content = request.POST['content']

    bull = BoradBulletin.objects.get(num=num)
    bull.title = title
    bull.content = content
    bull.save()

    return redirect("/lounge/bull/viewer/"+num+"/")


def bullDelete(request, num) :

    bull = BoradBulletin.objects.get(num=num)
    bull.delete()

    return redirect("/lounge/bull/list/1/")



def bullSaveComment(request) :

    comment = request.GET['comment']
    num = request.GET['num']
    userID = request.session['id']

    nowTime = timezone.now()

    print(num)

    save = BoradBulletinComment.objects.create(bulnum=str(num),userid=userID,content=comment,regtime=nowTime)

    return JsonResponse({"code": "0"})


def bullReloadComment(request) :
    num = request.GET['num']

    comment = BoradBulletinComment.objects.filter(bulnum=num).order_by("-num")

    return render(request, 'picktalk/ajax_comment.html', {'comment': comment})

def bullDeleteComment(request) :

    num = request.GET['num']

    comment = BoradBulletinComment.objects.get(num=num)
    comment.delete()

    return JsonResponse({"code": "0"})
