import re
import uuid
from datetime import datetime, timedelta, timezone

import requests
import json

import time
import uuid
import hmac
import hashlib

from math import sin, cos, sqrt, atan2, radians


R = 6373.0

SUCCESS = 1
FAIL = -1
AUTH_FAIL = -2
EXPIRED_KEY = -3
ID_DUP = -4
EMAIL_DUP = -5
RESIGN = -6
ID_NOT_EXIST = -7
PASSWORD_FAIL = -8
COMMUNITY_COMMENT_DUP = -9


NO_PERIOD = '상시모집'

MALE = 'MALE'
FEMALE = 'FEMALE'
NONE = 'NONE'

NORMAL = 'NORMAL'
COMPANY = 'COMPANY'


def send_fcm_notification(userSrls, title, body, type):
    # fcm 푸시 메세지 요청 주소
    url = 'https://fcm.googleapis.com/fcm/send'

    # 인증 정보(서버 키)를 헤더에 담아 전달
    headers = {
        'Authorization': 'key=AAAAQKm82g8:APA91bEb-kv9fUwl55I_m5iPA1ihC23TUCe1AKTlXmgeYf7MwjaW93GAlWZGREjAaaHCSPi-Pp17VWri3Eb-1eaqR6lDj7oF2JkE0b8M9-E3fDVnKJtwJuiNALs8OFzg9pKDSylMaxAx',
        'Content-Type': 'application/json; UTF-8',
    }

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


    # 보낼 내용과 대상을 지정
    # content = {
    #     'registration_ids': ids,
    #     'notification': {
    #         'title': title,
    #         'body': body,
    #     },
    #     'data': {
    #         'type': type,
    #         'userSrl': userSrl,
    #         'imageUrls': imageUrls,
    #         'time': timestamp,
    #         'isApproved': isApproved,
    #         'matchingSrl': matchingSrl,
    #     },
    #     'content_available': True,
    # }
    #
    # # json 파싱 후 requests 모듈로 FCM 서버에 요청
    # print('[PUSH_ALARM] to: ' + str(ids) + ' log: ' + requests.post(url, data=json.dumps(content), headers=headers).text)


def get_distance(lat1, lon1, lat2, lon2):
    lat1 = radians(float(lat1))
    lon1 = radians(float(lon1))
    lat2 = radians(float(lat2))
    lon2 = radians(float(lon2))

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance * 1000


def send_sms(to, text):     # 한글 45자, 영자 90자 이상 입력되면 자동으로 LMS타입의 문자메시자가 발송됩니다. type 옵션을 주어 명시적으로 타입을 지정할 수도 있습니다.
    data = {
        'message': {
            'to': str(to),
            'from': '01036381780',
            'text': str(text)  # 한글 45자, 영어 90자 이상이면 LMS로 자동 발송
        }
    }
    res = requests.post(get_url('/messages/v4/send'), headers=get_headers('NCSUUFB8PACUIGJH', '1MMGYSEEWLOGNQLRDHFSKDSOXRCA7YAW'), json=data)
    print(json.dumps(json.loads(res.text), indent=2, ensure_ascii=False))

    return True

prefix = ''

def get_url(path):
    url = '%s://%s' % ('https', 'api.coolsms.co.kr')
    if prefix != '':
        url = url + prefix
    url = url + path
    return url


def unique_id():
    return str(uuid.uuid1().hex)


def get_iso_datetime():
    utc_offset_sec = time.altzone if time.localtime().tm_isdst else time.timezone
    utc_offset = timedelta(seconds=-utc_offset_sec)
    return datetime.now().replace(tzinfo=timezone(offset=utc_offset)).isoformat()


def get_signature(key, msg):
    return hmac.new(key.encode(), msg.encode(), hashlib.sha256).hexdigest()


def get_headers(apiKey, apiSecret):
    date = get_iso_datetime()
    salt = unique_id()
    data = date + salt
    return {'Authorization': 'HMAC-SHA256 ApiKey=' + apiKey + ', Date=' + date + ', salt=' + salt + ', signature=' +
                             get_signature(apiSecret, data)}


def get_paging_index(page, size):
    page = int(page)
    size = int(size)
    return page * size, (page + 1) * size


def get_token_result(object):
    accessToken, accessTokenExpireDate = object.set_access_token()
    refreshToken, refreshTokenExpireDate = object.set_refresh_token()

    return {'accessToken': accessToken, 'accessTokenExpireDate': accessTokenExpireDate,
             'refreshToken': refreshToken, 'refreshTokenExpireDate': refreshTokenExpireDate}