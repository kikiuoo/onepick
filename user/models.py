import jwt
from django.contrib.auth.hashers import make_password, check_password
from django.db import models

# Create your models here.
from myonepick.settings import SECRET_KEY

from myonepick.common import *

# Create your models here.

SNS_TYPE = [
    ('카카오', '카카오'),
    ('구글', '구글'),
    ('애플', '애플'),
    ('페이스북', '페이스북'),
]

GENDER = [
    ('MALE', '남'),
    ('FEMALE', '여'),
    ('NONE', '무관')
]

USER_TYPE = [
    ('NORMAL', 'NORMAL'),
    ('COMPANY', 'COMPANY')
]


class User(models.Model):   # 유저 정보 필드들 중 사용하지 않는 필드들이 많으나 추후 사용될 것을 감안하여 추가해둔 필드 들이 있습니다. 예) email
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True, unique=True)
    nickname = models.CharField(max_length=100, null=True, blank=True)
    profileImage = models.ImageField(upload_to='photos/user/profile', null=True, blank=True)
    career = models.TextField(max_length=5000, default='', null=True, blank=True)
    description = models.CharField(max_length=1000, default='', null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER, default='MALE', null=True, blank=True)
    birth = models.CharField(max_length=20, null=True, blank=True)
    age = models.IntegerField(default=0, null=True, blank=True)
    foreigner = models.BooleanField(default=False)
    password = models.CharField(max_length=100, null=True, blank=True)
    snsUrl = models.CharField(max_length=500, null=True, blank=True)
    userType = models.CharField(max_length=50, choices=USER_TYPE, default='NORMAL', null=True, blank=True)

    point = models.FloatField(default=0, null=True, blank=True)

    agreeUsage = models.BooleanField(default=True)
    agreePrivacy = models.BooleanField(default=True)

    accessToken = models.CharField(max_length=200, null=True, blank=True)
    accessTokenExpireDate = models.DateTimeField(null=True, blank=True)
    refreshToken = models.CharField(max_length=200, null=True, blank=True)
    refreshTokenExpireDate = models.DateTimeField(null=True, blank=True)
    deviceId = models.CharField(max_length=200, null=True, blank=True)
    snsId = models.CharField(max_length=250, null=True, blank=True, unique=True)
    snsType = models.CharField(max_length=20, choices=SNS_TYPE, null=True, blank=True)
    fcmToken = models.CharField(max_length=1000, null=True, blank=True) # 푸쉬 알람용 토큰
    platform = models.TextField(max_length=100, null=True, blank=True)

    isApproved = models.BooleanField(default=False)
    isResign = models.BooleanField(default=False)
    isFirstLogin = models.BooleanField(default=True)
    isCertAdult = models.BooleanField(default=False)

    last_login = models.DateTimeField(auto_now_add=True, null=True)
    regTime = models.DateTimeField(auto_now_add=True)
    updTime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email if self.email else str(self.id)

    def store(self):
        self.save()
        return self

    def get_access_token(self):
        return self.accessToken

    def set_access_token(self):
        dt = datetime.now() + timedelta(days=10000)
        token = jwt.encode({
            'id': self.id,
            'exp': int(time.mktime(dt.timetuple()))
        }, SECRET_KEY, algorithm='HS256').decode('utf-8')
        self.accessToken = token
        self.accessTokenExpireDate = dt
        self.save()
        return token, dt

    def is_access_token_expired(self):
        return self.accessTokenExpireDate < datetime.now()

    def is_valid_access_token(self, token):
        if self.get_access_token() != token:
            return AUTH_FAIL
        if self.is_access_token_expired():
            return EXPIRED_KEY
        return SUCCESS

    def get_refresh_token_expire_date(self):
        return self.refreshToken, self.refreshTokenExpireDate

    def set_refresh_token(self):
        dt = datetime.now() + timedelta(days=6000)
        token = jwt.encode({
            'id': self.id,
            'exp': int(time.mktime(dt.timetuple()))
        }, SECRET_KEY, algorithm='HS256').decode('utf-8')
        self.refreshToken = token
        self.refreshTokenExpireDate = dt
        self.save()
        return token, dt

    def is_refresh_token_expired(self):
        return self.refreshTokenExpireDate < datetime.now()

    def is_valid_refresh_token(self, token):
        if self.refreshToken != token:
            return AUTH_FAIL
        if self.is_refresh_token_expired():
            return EXPIRED_KEY
        return SUCCESS

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password
        self.save()

    def check_password(self, raw_password):
        """
        Return a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """
        def setter(raw_password):
            self.set_password(raw_password)
            # Password hash upgrades shouldn't be considered password changes.
            self._password = None
            self.save(update_fields=["password"])
        return check_password(raw_password, self.password, setter)

    def is_under_19(self):
        now = datetime.now()
        birth = datetime.strptime(self.birth, '%Y-%m-%d')
        return (now - birth).days < 19 * 365

    def get_default_profile(self):
        return self.profiles.filter(isDefault=True).last()