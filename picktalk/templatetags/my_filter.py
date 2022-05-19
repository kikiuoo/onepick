from django import template
from django.utils import timezone
from django.db import connection

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

    returnValue = values[0:1]

    for i in range(count-1) :
        returnValue = returnValue + "*"

    return returnValue

@register.filter
def userAge(values):
    birth = values.split('-')
    nowTime = str(timezone.now())
    year = nowTime.split('-')

    age = int(year[0]) - int(birth[0]) + 1

    return age

@register.filter
def userHight(values) :
    hight = str(values).split('.')
    returnData = hight[0][:-1]

    return returnData + "*"

@register.filter
def parsingYoutube(values) :
    youtubeUrl = values.replace('https://youtu.be/', 'https://www.youtube.com/embed/' )
    return youtubeUrl

@register.filter
def getTalent(values) :
    talent = values.split('|')

    returnDate = ""
    count = 0;
    for talents in talent :
        count = count + 1
        returnDate = returnDate + " " + talents

        if count > 3 : break

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
            returnData = row[0] + "|" + row[1]
            
        if returnData == "" :
            returnData = "경력없음"

        connection.commit()
        connection.close()

    except:
        connection.rollback()
    return returnData