from django import template

register = template.Library()
from picktalk.templatetags.my_filter import *

