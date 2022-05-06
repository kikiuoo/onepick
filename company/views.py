from django.shortcuts import render

# Create your views here.
from django.contrib.sites import requests
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import boto3
from django.conf import settings
from django.utils import timezone
from picktalk.models import *


session = boto3.Session(
    aws_access_key_id = settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY,
)

def regCompany(request) :
    return render(request, 'company/regCompany.html')


def regCompanyCallBack(request) :

    userID = request.POST['userID']
    logo = request.FILES['logo']
    regImage = request.FILES['regImage']
    companyName = request.POST['companyName']
    registration = request.POST['registration']
    addr1 = request.POST['addr1']
    addr2 = request.POST['addr2']
    name = request.POST['name']
    phone1 = request.POST['phone1']
    phone2 = request.POST['phone2']
    phone3 = request.POST['phone3']
    webSite = request.POST['webSite']

    logoFileName = userID + "_logo_" + logo.name
    reqImageName = userID + "_reg_" +regImage.name

    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )

    s3_client.upload_fileobj(
        logo,
        settings.AWS_STORAGE_BUCKET_NAME,
        "media/photos/company/"+logoFileName,
        ExtraArgs={
            "ContentType": logo.content_type,
        }
    )

    s3_client.upload_fileobj(
        regImage,
        settings.AWS_STORAGE_BUCKET_NAME,
        "media/photos/company/" + reqImageName,
        ExtraArgs={
            "ContentType": regImage.content_type,
        }
    )

    nowTime = timezone.now()

    isCompany = UserCompany.objects.filter( userid=userID )

    print(isCompany)

    if isCompany.count() > 0 :
        for company in isCompany :
            company.logoimage = "photos/company/"+logoFileName
            company.licenseimage = "photos/company/" + reqImageName
            company.license = registration
            company.companyname = companyName
            company.addr1 = addr1
            company.addr2 = addr2
            company.phone = phone1+phone2+phone3
            company.updtime = nowTime
            company.website = webSite
            company.save()
    else :
        saveCompany = UserCompany.objects.create(userid=userID, logoimage="photos/company/"+logoFileName,
                                                 licenseimage="photos/company/" + reqImageName, license=registration,
                                                 companyname=companyName, addr1=addr1, addr2=addr2, name=name,
                                                 phone=phone1+phone2+phone3, website=webSite, regtime=nowTime)

    updateUser = UserInfo.objects.get(userid=userID)
    updateUser.usertype = "S-COMPANY"
    updateUser.save()

    return redirect('/')