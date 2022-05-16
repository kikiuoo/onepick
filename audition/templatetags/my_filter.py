from django import template

register = template.Library()

@register.filter
def findArrayData(values, list):
    if values in list:
        return "1"
    else :
        return "0"
