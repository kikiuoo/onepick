import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template import  loader
from django.db import connection

from picktalk.models import *
from django.db.models import Q
from django.utils import timezone

from myonepick.common import *

urlBase = "onepickAdmin/display/"

def audiList(request):

    audiType = request.GET.get('audiType', "")

    #recommend =

    return render( request, urlBase + "audiList.html", {'pageType': "display" })

