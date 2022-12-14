import requests
import hashlib
import random
from django.shortcuts import render, redirect

from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from picktalk.models import *
from myonepick.common import *

loginUrl = "https://myonepick.com/"
#loginUrl = "http://localhost:8000/"


def md5_generator(str):
    m = hashlib.md5()
    m.update(str.encode())
    return m.hexdigest()

# Create your views here.
def kakao_login(request):

    nUrl = nowDevice(request)

    client_id = "fed078068136559dc83c4f5f40362e5f"
    redirect_uri = loginUrl + "/login/kakao/callback/"

    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )

def kakao_login_callback(request):

    nUrl = nowDevice(request)

    code = request.GET.get("code", None)
    client_id = "fed078068136559dc83c4f5f40362e5f"
    redirect_uri = loginUrl + "/login/kakao/callback/"

    request_access_token = requests.post(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}",
        headers={"Accept": "application/json"},
    )

    access_token = request_access_token.json().get('access_token')
    user_info_response = requests.get('https://kapi.kakao.com/v2/user/me', headers={"Authorization" : f'Bearer ${access_token}'})

    profile_json = user_info_response.json()
    kakao_account = profile_json.get("kakao_account")

    id = str(profile_json.get("id"))
    email = kakao_account.get("email", None)

    returnUrl = userLogin(request, "kakao_"+id, email, "", "", "", "KAKAO")

    return redirect(returnUrl)




# 구글 로그인 API 호출
def googleLogin(request):
    nUrl = nowDevice(request)

    app_key = "329992018312-vcfcr44dgjat5q47pf91902rp8hh1ei0.apps.googleusercontent.com"
    scope = "https://www.googleapis.com/auth/userinfo.email " + \
            "https://www.googleapis.com/auth/userinfo.profile"

    redirect_uri = loginUrl + "/login/google/callback/"
    google_auth_api = "https://accounts.google.com/o/oauth2/v2/auth"

    response = redirect(
        f"{google_auth_api}?client_id={app_key}&response_type=code&redirect_uri={redirect_uri}&scope={scope}"
    )

    return response


# 구글 로그인 처리.
def googleLoginCallback(request):
    nUrl = nowDevice(request)

    code = request.GET.get('code')
    client_id = "329992018312-vcfcr44dgjat5q47pf91902rp8hh1ei0.apps.googleusercontent.com"
    client_secret = "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"
    #AIzaSyDK6_FmteverNdo8r3womycHKb8MbboFbo

    redirection_uri = loginUrl + "/login/google/callback/"
    grant_type = 'authorization_code'
    state = "random_string"

    request_access_token = requests.post(
         f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type={grant_type}&redirect_uri={redirection_uri}&state={state}"
    )

    access_token = request_access_token.json().get('access_token')

    user_info_response = requests.get( "https://www.googleapis.com/oauth2/v3/userinfo",
        params={ 'access_token': access_token  }  )

    profile_json = user_info_response.json()

    sub = profile_json.get("sub")
    email = profile_json.get("email")
    print(sub + " " + email)

    returnUrl = userLogin(request, "google_"+sub, email, "", "", "", "GOOGLE")

    return redirect(returnUrl)


def naver_login(request):
    nUrl = nowDevice(request)

    client_id = "0HGf7pdIAXwsh0Jvwa6_"
    redirect_uri = loginUrl + "/login/naver/callback/"

    print(f"https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&state=RAMDOM_STATE")
    return redirect(
        f"https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&state=RAMDOM_STATE"
    )

def naver_login_callback(request):
    nUrl = nowDevice(request)

    code = request.GET.get("code", None)
    state = request.GET.get("state", None)
    client_id = "0HGf7pdIAXwsh0Jvwa6_"
    client_secret = "_5rS6cXipg"
    redirect_uri = loginUrl + "/login/naver/callback/"

    request_access_token = requests.post(
        f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&redirect_uri={redirect_uri}&code={code}&state={state}",
        headers={"Accept": "application/json"},
    )

    access_token = request_access_token.json().get('access_token')
    user_info_response = requests.get('https://openapi.naver.com/v1/nid/me?token_type=access_token&access_token='+access_token)

    profile_json = user_info_response.json()
    response = profile_json.get("response")

    id = response.get("id")

    returnUrl = userLogin(request, "naver_"+id, "", "", "", "", "NAVER")

    return redirect(returnUrl)


def localLogin (request) :

    nUrl = nowDevice(request)
    reUrl = request.GET.get('reUrl',"")

    return render(request, nUrl + '/login/login.html', {"reUrl":reUrl})

def localLoginCallback (request) :
    username = request.GET['username']
    password = request.GET['password']

    pw = md5_generator(password)
    userIN = UserInfo.objects.filter(userid=username, password=pw)

    if userIN.count() > 0:
        userIN = UserInfo.objects.get(userid=username, password=pw)

        request.session['id'] = userIN.userid
        request.session['userType'] = userIN.usertype

        request.session.set_expiry(0)

        updateLastVisit(userIN.userid)

        return JsonResponse({"code": "0"})
    else:
        return JsonResponse({"code": "1", 'message': "아이디 혹은 비밀번호가 일치 하지 않습니다."})


def userLogin(request, id, email, gender, name, birth, joinType) :

    nUrl = nowDevice(request)

    returnUrl = ""
    isUser = UserInfo.objects.filter(userid=id)

    if isUser.count() <= 0 :
        nowTime = timezone.now()
        #addUser = UserInfo.objects.create(userid=id, email=email, jointype=joinType, gender=gender, name=name,
        #                                  birth=birth, regtime=nowTime, lastlogin=nowTime, logincount=1,
        #                                  usertype="NORMAL")
        key = id

        returnUrl =  "/login/socialAgree/" + str(key) + "/"
    else :
        isUser = UserInfo.objects.get(userid=id)

        userID = isUser.userid
        userType = isUser.usertype

        request.session['id'] = userID
        request.session['userType'] = userType
        request.session.set_expiry(0)

        updateLastVisit(userID)
        returnUrl = "/"


    return returnUrl


def locallogout (request) :
    del request.session['id']
    del request.session['userType']

    return JsonResponse({"code": "0"} )


def updateLastVisit(userID) :
    nowTime = timezone.now()

    updateTime = UserInfo.objects.get(userid = userID)
    updateTime.logincount = updateTime.logincount + 1
    updateTime.lastlogin = nowTime
    updateTime.save()

    insertLogin = UserLogin.objects.create(userid=userID, accesstime=nowTime)

    return ""

def joinView(request) :

    nUrl = nowDevice(request)

    return render(request, nUrl + '/login/joinView.html')

# 기업회원 회원가입 약관.
def joinAgreementC(request) :

    nUrl = nowDevice(request)

    return render(request, nUrl + '/login/agreementC.html')

# 일반회원 회원가입 약관.
def socialAgree(request, userID) :

    nUrl = nowDevice(request)

    return render(request, nUrl + '/login/socialAgree.html', {"userID": userID})



def joinSocial(request, userID) :

    nUrl = nowDevice(request)

    returnUrl = ""
    isUser = UserInfo.objects.filter(userid=userID)

    if isUser.count() <= 0 :
        nowTime = timezone.now()
        addUser = UserInfo.objects.create(userid=userID,  agreeusage="1", agreeprivacy="1",agreemarketing="1",
                                          regtime=nowTime, lastlogin=nowTime, logincount=1, jointype="SOCIAL", usertype="NORMAL" )


    request.session['id'] = userID
    request.session['userType'] = "NORMAL"
    request.session.set_expiry(0)

    updateLastVisit(userID)

    return redirect("/")



def joinCompany(request) :

    nUrl = nowDevice(request)

    return render(request, nUrl + '/login/joinCompany.html')

@csrf_exempt
def joinCompanyCallback(request):
    nUrl = nowDevice(request)

    userID = request.POST.get('user_id',"")
    pw1 = request.POST.get('pw1',"")
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']

    companyName = request.POST.get('companyName',"")
    license = request.POST.get('license',"")
    companyAddr1 = request.POST.get('companyAddr1',"")
    companyAddr2 = request.POST.get('companyAddr2',"")
    webSite = request.POST.get('webSite',"")
    logo = request.FILES.getlist('logo[]')
    licenseImage = request.FILES.getlist('licenseImage[]')
    artLicense = request.FILES.getlist('artLicense[]')

    phoneCheck = request.POST.get('phoneCheck',"")
    emailCheck = request.POST.get('emailCheck',"")

    if phoneCheck != "1" :
        phoneCheck = "0"

    if emailCheck != "1":
        emailCheck = "0"

    nowTime = timezone.now()

    saveUserInfo = UserInfo.objects.create(
                    userid=userID, password=md5_generator(pw1), name=name, email=email, phone=phone,
                    birth="-", addr1=companyAddr1, addr2=companyAddr2, agreeusage="1", agreeprivacy="1", jointype="OLDUSER",
                    agreemarketing="1", agreeemail=emailCheck, agreesms=phoneCheck, regtime=nowTime, usertype="S-COMPANY", logincount=0 )

    count = 0
    # 로고
    for image in logo:
        count = count + 1
        sub = image.name.split('.')[-1]
        url = uploadFile(image, "photos/company/", sub)
        logoImage = url

    count = 0
    for image in licenseImage:
        count = count + 1
        sub = image.name.split('.')[-1]
        url = uploadFile(image, "photos/company/", sub)
        licenseImages = url

    count = 0
    for image in artLicense:
        count = count + 1
        sub = image.name.split('.')[-1]
        url = uploadFile(image, "photos/company/", sub)
        artLicenses = url


    userCompany = UserCompany.objects.create(userid=userID, logoimage=logoImage, licenseimage=licenseImages, artlicenseimage=artLicenses,
                                             license=license,companyname=companyName, addr1=companyAddr1, addr2=companyAddr2, website=webSite,
                                             regtime=nowTime)

    send = sendSMS("01026324446", "기업회원 가입", "[ONEPICK 기업가입] "+companyName+"` 기업이 새로 가입했습니다.")

    return redirect("/")




def joinUser(request) :

    nUrl = nowDevice(request)

    user = request.session.get('id', '')
    userInfo = UserInfo.objects.get(userid=user)

    return render(request, nUrl + '/login/joinUser.html', {"userInfo":userInfo})

@csrf_exempt
def joinUserCallback(request):

    userID = request.POST.get('user_id',"")
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    birth = request.POST.get('birth',"")
    gender = request.POST.get('gender',"")
    companyAddr1 = request.POST.get('companyAddr1',"")
    companyAddr2 = request.POST.get('companyAddr2',"")
    phoneCheck = request.POST.get('phoneCheck',"")
    emailCheck = request.POST.get('emailCheck',"")

    if phoneCheck != "1" :
        phoneCheck = "0"

    if emailCheck != "1":
        emailCheck = "0"


    userInfo = UserInfo.objects.get(userid=userID)

    userInfo.name = name
    userInfo.email = email
    userInfo.phone = phone
    userInfo.birth = birth
    userInfo.gender = gender
    userInfo.addr1 = companyAddr1
    userInfo.addr2 = companyAddr2
    userInfo.agreeemail = emailCheck
    userInfo.agreesms = phoneCheck
    userInfo.usertype = "NORMAL"
    userInfo.save()


    return redirect("/")




# 회원가입.
def join(request, userID, type) :

    nUrl = nowDevice(request)
    user = UserInfo.objects.get(userid=userID)

    return render(request, nUrl + '/login/join.html', {'user': user, 'type': type})


@csrf_exempt
def joinUpdate(request):
    nUrl = nowDevice(request)

    num = request.POST['num']
    joinType = request.POST['joinType']
    userType = request.POST.get('userType',"")
    userID = request.POST.get('user_id',"")
    oldUserID = request.POST.get('oldUserID',"")
    pw1 = request.POST.get('pw1',"")
    name = request.POST['name']
    email1 = request.POST['email1']
    email2 = request.POST['email2']
    phone1 = request.POST['phone1']
    phone2 = request.POST['phone2']
    phone3 = request.POST['phone3']
    brith1 = request.POST.get('brith1',"")
    brith2 = request.POST.get('brith2',"")
    brith3 = request.POST.get('brith3',"")
    gender = request.POST.get('gender',"")
    addr1 = request.POST.get('addr1',"")
    addr2 = request.POST.get('addr2',"")
    companyName = request.POST.get('companyName',"")
    license = request.POST.get('license',"")
    companyAddr1 = request.POST.get('companyAddr1',"")
    companyAddr2 = request.POST.get('companyAddr2',"")
    webSite = request.POST.get('webSite',"")
    logo = request.FILES.getlist('logo[]')
    licenseImage = request.FILES.getlist('licenseImage[]')
    artLicense = request.FILES.getlist('artLicense[]')

    phoneCheck = request.POST.get('phoneCheck',"")
    emailCheck = request.POST.get('emailCheck',"")

    if phoneCheck != "1" :
        phoneCheck = "0"

    if emailCheck != "1":
        emailCheck = "0"

    print ( oldUserID )

    if oldUserID == "" :
        userInfo = UserInfo.objects.get(num=num)
    else :
        userInfo = UserInfo.objects.get(userid=oldUserID)
        updateUserID(userID, oldUserID)

    if joinType == "oldUser" :
        userInfo.password = md5_generator(pw1)
        userInfo.jointype = "OLDUSER"

    userInfo.name = name
    userInfo.email = email1+"@"+email2
    userInfo.phone = phone1+phone2+phone3
    userInfo.gender = gender
    userInfo.birth = brith1+"-"+brith2+"-"+brith3

    userInfo.agreeusage = "1"
    userInfo.agreeprivacy = "1"
    userInfo.agreemarketing = "1"
    userInfo.agreeemail = emailCheck
    userInfo.agreesms = phoneCheck

    if userType == "NORMAL" or  userType == "S-NORMAL" :
        # 일반회원 등록
        userInfo.addr1 = addr1
        userInfo.addr2 = addr2
        userInfo.usertype = "NORMAL"
    else :
        userInfo.usertype = "S-COMPANY"

        nowTime = timezone.now()

        count = 0
        # 로고
        logoImage = ""
        for image in logo:
            count = count + 1
            sub = image.name.split('.')[-1]
            url = uploadFile(image, "photos/company/", sub)
            logoImage = url

        count = 0
        licenseImages = ""
        for image in licenseImage:
            count = count + 1
            sub = image.name.split('.')[-1]
            url = uploadFile(image, "photos/company/", sub)
            licenseImages = url

        count = 0
        artLicenses = ""
        for image in artLicense:
            count = count + 1
            sub = image.name.split('.')[-1]
            url = uploadFile(image, "photos/company/", sub)
            artLicenses = url


        userCompany = UserCompany.objects.create(userid=userID, logoimage=logoImage, licenseimage=licenseImages, artlicenseimage=artLicenses,
                                                 license=license,companyname=companyName, addr1=companyAddr1, addr2=companyAddr2, website=webSite,
                                                 regtime=nowTime)

    userInfo.save()

    return redirect("/" + nUrl + "/")



# id, pw 찾기
def finduser(request) :

    nUrl = nowDevice(request)

    return render(request, nUrl + '/login/findUser.html')

def findPW (request) :
    if request.method == "GET" :
        return JsonResponse({"code": "1", "message" : "잘못된 접근입니다."})
    elif request.method == "POST" :
        userID = request.POST['userID']
        userPhone = request.POST['userPhone']

        userIN = UserInfo.objects.filter(userid=userID, phone=userPhone)

        if userIN.count() > 0 :
            return JsonResponse({"code": "0"} )
        else :
            return JsonResponse({"code": "1", 'message' : "아이디와 이름이 일치하는 정보가 없습니다."})

    else:
        return JsonResponse({"code": "1", "message": "잘못된 접근입니다."})

def updatePW_local(request) :

    if request.method == "GET" :
        userID = request.GET['userID']
        password = request.GET['password']

        print(userID)

        userIN = UserInfo.objects.get(userid=userID)
        userIN.password = md5_generator(password)

        if userIN.usertype == "S-NORMAL" :
            userIN.usertype = "NORMAL"

        userIN.save()

        return JsonResponse({"code": "0"} )
    else:
        return JsonResponse({"code": "1", "message": "잘못된 접근입니다."})


def ajax_findOldUser(request) :

    nUrl = nowDevice(request)

    userName = request.GET.get("userName","")
    userPhone = request.GET.get("userPhone","")

    userInfo = UserInfo.objects.filter(name=userName, phone=userPhone, usertype="S-NORMAL")

    return render(request, nUrl + '/login/ajax_findOldUser.html', {'userInfo': userInfo })


def ajax_findUser(request) :

    nUrl = nowDevice(request)

    userName = request.GET.get("userName","")
    userPhone = request.GET.get("userPhone","")

    userInfo = UserInfo.objects.filter(name=userName, phone=userPhone)

    userID = ""
    userType = ""
    if len(userInfo) == 0 :
        return JsonResponse({"code": "1", "message" : "회원정보를 찾을 수 없습니다." })
    else :
        for user in userInfo :
            userID = user.userid
            userType = user.jointype

    return JsonResponse({"code": "0", "userID" : userID, "userType" : userType })



def ajax_idFindPhoneComfirm(request) :

    userPhone = request.GET.get("phoneNum","")
    certifier = ""

    while len(certifier) < 4:
        num = random.randint(0, 9)
        certifier = certifier + str(num)

    nowTime = timezone.now()
    saveSms = UserSms.objects.create(phonenum=userPhone, certifier=certifier, regdate=nowTime)

    send = sendSMS(userPhone, "인증번호 전송", "[ONEPICK 본인확인] 인증번호 [" + certifier + "]를 입력해주세요.")

    return JsonResponse({"code": "0"})



def ajax_phoneComfirm(request) :

    userPhone = request.GET.get("phoneNum","")
    certifier = ""

    isUser = UserInfo.objects.filter(phone=userPhone, usertype="NORMAL") | UserInfo.objects.filter(phone=userPhone, usertype="COMPANY")  | UserInfo.objects.filter(phone=userPhone, usertype="S-COMPANY")

    if isUser.count() > 0 :
        return JsonResponse({"code": "1", "message" :  "이미 등록된 전화번호입니다."})
    else :
        while len(certifier) < 4:
            num = random.randint(0, 9)
            certifier = certifier + str(num)

        nowTime = timezone.now()
        saveSms = UserSms.objects.create(phonenum=userPhone, certifier=certifier, regdate=nowTime)

        send = sendSMS(userPhone, "인증번호 전송", "[ONEPICK 본인확인] 인증번호 [" + certifier + "]를 입력해주세요.")

        return JsonResponse({"code": "0"})

def ajax_pwPhoneComfirm(request) :

    userID = request.GET.get("userID","")
    userPhone = request.GET.get("phoneNum","")
    certifier = ""

    isUser = UserInfo.objects.filter(userid=userID, phone=userPhone)

    if isUser.count() > 0 :
        while len(certifier) < 4:
            num = random.randint(0, 9)
            certifier = certifier + str(num)

        nowTime = timezone.now()
        saveSms = UserSms.objects.create(phonenum=userPhone, certifier=certifier, regdate=nowTime)

        send = sendSMS(userPhone, "인증번호 전송", "[ONEPICK 본인확인] 인증번호 [" + certifier + "]를 입력해주세요.")

        return JsonResponse({"code": "0"})
    else :
        return JsonResponse({"code": "1", "message" :  "아이디, 전화번호를 확인해주세요."})


def ajax_checkConfirm(request) :

    userPhone = request.GET.get("phoneNum","")
    confirm = request.GET.get("confirm","")

    findSMS = UserSms.objects.filter(phonenum=userPhone).order_by("-num")[:1]

    saveConfirm = ""
    for row in findSMS :
        saveConfirm = row.certifier

    code = ""
    msg = ""
    if confirm == saveConfirm :
        findSMS = UserSms.objects.filter(phonenum=userPhone).order_by("-num")
        findSMS.delete()
        code = "0"
    else :
        code = "1"
        msg = "입력한 인증번호가 다릅니다."

    return JsonResponse({"code": code, "message" :  msg})


def ajax_checkOverlapID(request) :

    userID = request.GET.get("userID","")

    findUser = UserInfo.objects.filter(userid=userID)

    if len(findUser) > 0 :
        code = "1"
        msg = "이미 등록된 아이디입니다."
        
    else :
        code = "0"
        msg = ""

    return JsonResponse({"code": code, "message" :  msg})



def comfirmPhone(requset):

    return "/"

def updateUserID(userID, oldUserID) :

    userdel = UserInfo.objects.filter(userid=userID)
    userdel.delete()
    userInfo = UserInfo.objects.filter(userid=oldUserID)
    for row in userInfo :
        row.userid = userID
        row.save()

    userCompany = UserCompany.objects.filter(userid=oldUserID).update(userid=userID)
    audiInfo = AuditionInfo.objects.filter(userid=oldUserID).update(userid=userID)
    audiPick = AuditionPick.objects.filter(userid=oldUserID).update(userid=userID)

    proCareer = ProfileCareer.objects.filter(userid=oldUserID).update(userid=userID)
    proComment = ProfileComment.objects.filter(userid=oldUserID).update(userid=userID)
    proEtcCar = ProfileEtccareer.objects.filter(userid=oldUserID).update(userid=userID)
    proInfo = ProfileInfo.objects.filter(userid=oldUserID).update(userid=userID)
    proPick = ProfilePick.objects.filter(userid=oldUserID).update(userid=userID)

    qaQandA = QaQanda.objects.filter(userid=oldUserID).update(userid=userID)
    qaComment = QaQandaComment.objects.filter(userid=oldUserID).update(userid=userID)

    return ""