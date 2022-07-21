import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template import  loader
from django.db import connection

from picktalk.models import *
from django.conf import settings
from django.utils import timezone

from myonepick.common import *


def adminCheck(request): # 오디션 Main

    user = request.session.get('adminID', '')

    returnURL = "onepickAdmin/login/login.html"

    if user :
        returnURL = "onepickAdmin/main.html"

    return render(request, returnURL )
