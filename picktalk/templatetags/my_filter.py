from django import template
from django.utils import timezone

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

    return hight[0][0:2] + "*"