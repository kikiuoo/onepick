from django import template
from django.utils import timezone
from django.db import connection
import math

from picktalk.models import *

register = template.Library()

@register.filter
def findArrayData(values, list):
    if values in list:
        return "1"
    else :
        return "0"


@register.filter
def updateUserName(values):
    count = len(values)

    returnValue = values[:-1]

    returnValue = returnValue + "*"

    return returnValue

@register.filter
def userAge(values):
    if values != None :
        birth = values.split('-')
        nowTime = str(timezone.now())
        year = nowTime.split('-')

        if birth[0] != "" :
            age = int(year[0]) - int(birth[0]) + 1
        else :
            age = "-"
    else :
        age = "-"

    return age

@register.filter
def userHight(values) :
    hight = str(values).split('.')
    returnData = hight[0][:-1]

    return returnData + "*"

@register.filter
def parsingYoutube_view(values) :
    if values == None :
        youtubeUrl = "";
    else :
        youtubeUrl = values.replace('https://youtu.be/', 'https://www.youtube.com/embed/' )
    return youtubeUrl

@register.filter
def getTalent(values) :

    print(values)

    if values != None and values != "" :
       talent = values.split('|')

       returnDate = ""
       count = 0;
       for talents in talent :
            count = count + 1
            returnDate = returnDate + " " + talents

            if count > 3 : break
    else :
        returnDate = ""

    return returnDate

@register.filter
def getCareer(num, type) :
    try:
        cursor = connection.cursor()

        query = "SELECT title, ROLE   " \
                "FROM profile_career AS pc LEFT JOIN cate_sub AS cs " \
                "     ON pc.cateSubType = cs.subCate " \
                "WHERE profileNum = '"+ str(num) +"' and otherGroup = '"+type+"' " \
                "order by pc.num desc limit 1"


        result = cursor.execute(query)
        career = cursor.fetchall()

        returnData = ""
        for row in career :
            returnData = row[0] + "ㅣ" + row[1]
            
        if returnData == "" :
            returnData = "경력없음"

        connection.commit()
        connection.close()

    except:
        connection.rollback()
    return returnData

@register.filter
def replace(value, keys):
    if value == None :
        return ""
    key = keys.split("|")
    returnValue = value.replace(key[0], key[1])
    return returnValue

@register.filter
def replace_2(value, keys):
    key = keys.split(",")
    returnValue = value.replace(key[0], key[1])
    return returnValue

@register.filter
def allReplace(value, key):

    returnValue = ""
    for values in value :
        returnValue = returnValue + key

    return returnValue

@register.filter
def phoneReplace(value, key):

    returnValue = ""
    count = 0
    for values in value :

        if count == 3 or count == 7 :
            returnValue = returnValue + "-"

        if count < 5 :
            returnValue = returnValue + values
        else :
            returnValue = returnValue + key
        count = count + 1;

    return returnValue

@register.filter
def emailReplace(value, key):

    email = value.split("@")
    returnValue = ""

    count = 0
    for values in email[0] :
        if count == 0:
            returnValue = returnValue + values
        else:
            returnValue = returnValue + key
        count = count + 1;

    if len(email) >= 2 :
        returnValue = returnValue + "@" + email[1]
    else :
        returnValue = value

    return returnValue



@register.filter
def getMainCate(value):

    if value == None :
        return ""

    cate = CateMain.objects.get(catecode=value)

    return cate.catename


@register.filter
def getSubCate(value):

    if value == None :
        return ""

    cate = CateSub.objects.get(subcate=value)

    return cate.catename


@register.filter
def getSubCates(value):

    subCate = value.split("|")

    returnValue = []
    for cate in subCate :
        cates = CateSub.objects.get(subcate=cate)
        returnValue.append(cates.catename)

    sCate = ", ".join(returnValue)

    return sCate

@register.filter
def getArrayCount(value):

    returnLen = 0;
    if value != "" :
        returnLen = len(value)

    return returnLen

@register.filter
def getUserName(valuse):
    print(" 아이디 : " + valuse)

    user = UserInfo.objects.filter(userid=valuse)

    returnValue = ""

    if user.count() > 0 :
        for row in user :
            userName = row.name

            count = 0
            for values in userName:
                if count == 0 or count == (len(userName)-1):
                    returnValue = returnValue + values
                else:
                    returnValue = returnValue + "*"
                count = count + 1;

    else :
        returnValue = '***'

    return returnValue

@register.filter
def getUserFullName(valuse):

    user = UserInfo.objects.filter(userid=valuse)

    userName = ""
    if user.count() > 0 :
        for row in user :
            userName = row.name

    else :
        userName = '***'

    return userName

@register.filter
def addNum(value, addValue) :
    returnNum = int(value) + int(addValue)

    return returnNum

@register.filter
def parsingCareer(value) :

    returnData = ""

    #profileNum, title, ROLE, cm.cateName AS mainCate, cs.cateName AS subCate

    print( value )

    count = 0;
    for values in value :
        saveData = values[5] + "$" + values[3] + "$" + values[6] + "$" +  values[4] + "$"  +  values[1] + "$" + values[2]
        if count == 0 :
            returnData = returnData + saveData
        else :
            returnData = returnData + "|" + saveData
        count = count + 1

    return returnData

@register.filter
def parsingYoutube(value) :

    returnData = ""

    #count, link
    count = 0;
    for values in value :
        saveData = "s" + str(count) +  "$" + values
        if count == 0 :
            returnData = returnData + saveData
        else :
            returnData = returnData + "|" + saveData
        count = count + 1

    return returnData

@register.filter
def parsingETCCareer(value) :

    returnData = ""

    #ec_cateM + "$" + ec_cateS + "$" + ec_title + "$" + ec_role
    count = 0;
    for values in value :
        saveData =  values.catetype +  "$" + values.subcatetype + "$" + values.title + "$" + values.role
        if count == 0 :
            returnData = returnData + saveData
        else :
            returnData = returnData + "|" + saveData
        count = count + 1

    return returnData

@register.filter
def getData(value, count) :

    data = value.split("$")

    return data[count]


@register.filter
def getPersent(num) :

    profile = ProfileInfo.objects.get(num=num)
    userInfo = UserInfo.objects.get(userid=profile.userid)

    count = 25;

    if userInfo.nationality == None or userInfo.nationality == ""  :
        count = count - 1

    if userInfo.military == None or userInfo.military == "" :
        count = count - 1

    if userInfo.entertain == None or userInfo.entertain == "" :
        count = count - 1

    if userInfo.finalschool == None or userInfo.finalschool == "" :
        count = count - 1

    if userInfo.school == None or userInfo.school == "" :
        count = count - 1

    if userInfo.major == None or userInfo.major == "" :
        count = count - 1

    if profile.height == None  or profile.height == "":
        count = count - 1

    if profile.weight == None  or profile.weight == "":
        count = count - 1

    if profile.topsize == None or profile.topsize == "" :
        count = count - 1

    if profile.bottomsize == None or profile.bottomsize == "":
        count = count - 1

    if profile.shoessize == None or profile.shoessize == "":
        count = count - 1

    if profile.skincolor == None or profile.skincolor == "":
        count = count - 1

    if profile.haircolor == None or profile.haircolor == "":
        count = count - 1

    if profile.intercate == None or profile.intercate == "":
        count = count - 1

    if profile.intersubcate == None or profile.intersubcate == "":
        count = count - 1

    if profile.iscareer != "0":
        career = ProfileCareer.objects.filter(profilenum=num)
        if career.count() < 0 :
            count = count - 1

    if profile.profileimage == None or profile.profileimage == "":
        count = count - 1

    if profile.detailimage == None or profile.detailimage == "":
        count = count - 1

    if profile.artimage == None or profile.artimage == "":
        count = count - 1

    if profile.youtube == None or profile.youtube == "":
        count = count - 1

    if profile.foreign == None or profile.foreign == "":
        count = count - 1

    if profile.talent == None or profile.talent == "":
        count = count - 1

    if profile.comment == None or profile.comment == "":
        count = count - 1

    etcCareer = ProfileEtccareer.objects.filter(profilenum=num)
    if etcCareer.count() < 0 :
        count = count - 1

    persent = (count / 25) * 100

    return round(persent)

@register.filter
def applyCount(num) :

    try:
        cursor = connection.cursor()

        query = "SELECT COUNT( DISTINCT(profileNum)) FROM audition_apply WHERE auditionNum = '"+str(num)+"' "

        result = cursor.execute(query)
        apply = cursor.fetchall()

        connection.close()

    except:
        connection.rollback()

    print(apply[0][0])

    return apply[0][0]


@register.filter
def audiListCate(cate) :
    cates = cate.split(",")
    return cates[0]

@register.filter
def splits(values, splitKey) :
    spl = splitKey.split("|")
    returnValue = str(values).split( str(spl[1]) )
    return returnValue[ int(spl[0]) ]

@register.filter
def userAddr(values) :
    if values == "" or values == None :
        return ""

    addr = values.replace(")", " ")
    addr = addr.replace("(", "")
    addr = addr.replace("  ", " ")

    if addr == "" :
        returnValue = "";
    else :
        addrs = addr.split(' ')
        print(addrs)

        if len(addrs) > 2 :
            returnValue = addrs[1] + " " + addrs[2];
        else :
            returnValue = "";

    return returnValue


@register.filter
def getCmmCount(values, table) :

    if table == "magazine" :
        comm = BoardMagazineComment.objects.filter(mgnum=values)

    elif table == "bulletin" :
        comm = BoradBulletinComment.objects.filter(bulnum=values)

    return len(comm)

@register.filter
def nowData(values, count):

    return values[count]



@register.filter
def findUserType(values):

    userInfo = UserInfo.objects.get(userid=values)

    return userInfo.usertype


@register.filter
def checkApply(values):

    try:
        cursor = connection.cursor()

        query = "SELECT * " \
                "FROM qa_qanda_comment AS qqc LEFT JOIN user_info AS ui " \
                "     ON qqc.userID = ui.userID " \
                "WHERE qaNum = '"+str(values)+"' AND userType = 'admin'"

        result = cursor.execute(query)
        qanda = cursor.fetchall()
        connection.commit()
        connection.close()

    except:
        connection.rollback()

    return len(qanda)

@register.filter
def modData(values) :

    nowData = int(values) % 2

    return nowData


@register.filter
def modData2(values) :

    nowData = int(values) % 4

    return nowData

@register.filter
def getFirstImage(values) :

    audiImage = values.split("|")

    return audiImage[0]