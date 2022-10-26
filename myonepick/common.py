from django.core.files.storage import FileSystemStorage
from django.utils import timezone
import hashlib
import os
import requests
from django.conf import settings
import datetime
import smtplib
from email.mime.text import MIMEText
from cryptography.fernet import Fernet # symmetric encryption

def getPageList ( nowPage, allPage) :

    sPage = nowPage - 2
    if sPage <= 0 :
        startPage = 1
    elif sPage + 4 > allPage :
        startPage = allPage - 4
    else :
        startPage = sPage

    ePage = 1
    if allPage < 5 :
        ePage = allPage
    elif startPage + 4 > allPage :
        ePage = allPage
    else :
        ePage = startPage + 4

    paging = list(range(int(startPage), int(ePage)+1))

    return paging



def getPageList_v2 ( nowPage, allPage) :

    if nowPage % 10 == 0 :
        pageArea = nowPage
    else :
        pageArea = int( (nowPage/10) + 1 ) * 10

    sPage = pageArea-9
    ePage = pageArea+1
    if int(allPage) < ePage:
        ePage = int(allPage) + 1

    paging = list(range(sPage, ePage))

    return paging



def  uploadFile(uploadFile, fileurl, sub):
    # Saving the information in the database
    fs = FileSystemStorage(location='media/'+fileurl, base_url='media/'+fileurl)
    # FileSystemStorage.save(file_name, file_content)

    nowTime = timezone.now()

    image = uploadFile.name + "_" + str(nowTime)
    image_url = md5_generator(image) + "." + sub

    filename = fs.save(image_url, uploadFile)
    uploaded_file_url = fs.url(filename)
    uploaded_file_url = uploaded_file_url.replace("media/", "")

    return uploaded_file_url

def deleteFile(uplad_files):
    os.remove(os.path.join(settings.MEDIA_ROOT, uplad_files))



def md5_generator(str):
    m = hashlib.md5()
    m.update(str.encode())
    return m.hexdigest()


def sendSMS( receiver, title, msg ) :

    send_url = 'https://apis.aligo.in/send/'  # 요청을 던지는 URL, 현재는 문자보내기

    # ================================================================== 문자 보낼 때 필수 key값
    # API key, userid, sender, receiver, msg
    # API키, 알리고 사이트 아이디, 발신번호, 수신번호, 문자내용

    sms_data = {'key': 'cl40fh7a45efop5rdoz2vhyqpizi5eus',  # api key
                'userid': 'ksnpick',  # 알리고 사이트 아이디
                'sender': '0234424440',  # 발신번호
                'receiver': receiver,  # 수신번호 (,활용하여 1000명까지 추가 가능)
                'msg': msg,  # 문자 내용
                'msg_type': title,  # 메세지 타입 (SMS, LMS)
                'title': 'title',  # 메세지 제목 (장문에 적용)
                'destination': receiver,  # %고객명% 치환용 입력
                # 'rdate' : '예약날짜',
                # 'rtime' : '예약시간',
                # 'testmode_yn' : '' #테스트모드 적용 여부 Y/N
                }
    send_response = requests.post(send_url, data=sms_data)

    return send_response.json()


def finalDate(date) :

    print(date)

    if date == "" or date == None : return ""

    endDate = str(date).split(" ");
    lastDate = endDate[0].split("-")

    today = datetime.date.today()
    target_date = datetime.date(int(lastDate[0]), int(lastDate[1]), int(lastDate[2]))

    d_day = target_date - today

    return d_day.days


def sendMails(title, content, mail) :
    try :
        print( title+ " " +  content + " " + mail)

        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.ehlo()
        smtp.starttls()
        smtp.login("ksonepick@gmail.com", "cfbfdpogjnchjrvk")  # 로그인 정보

        msg = MIMEText(content, 'html')
        msg['Subject'] = title

        smtp.sendmail("ksonepick@gmail.com", mail, msg.as_string())
        smtp.quit()

    except :
        return "FAIL"
    return "OK"


class SimpleEnDecrypt:
    def __init__(self, key=None):
        if key is None:  # 키가 없다면
            key = Fernet.generate_key()  # 키를 생성한다
        self.key = key
        self.f = Fernet(self.key)

    def encrypt(self, data, is_out_string=True):
        if isinstance(data, bytes):
            ou = self.f.encrypt(data)  # 바이트형태이면 바로 암호화
        else:
            ou = self.f.encrypt(data.encode('utf-8'))  # 인코딩 후 암호화
        if is_out_string is True:
            return ou.decode('utf-8')  # 출력이 문자열이면 디코딩 후 반환
        else:
            return ou

    def decrypt(self, data, is_out_string=True):
        if isinstance(data, bytes):
            ou = self.f.decrypt(data)  # 바이트형태이면 바로 복호화
        else:
            ou = self.f.decrypt(data.encode('utf-8'))  # 인코딩 후 복호화
        if is_out_string is True:
            return ou.decode('utf-8')  # 출력이 문자열이면 디코딩 후 반환
        else:
            return ou