# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class AuditionApply(models.Model):
    num = models.BigAutoField(primary_key=True)
    auditionnum = models.PositiveBigIntegerField(db_column='auditionNum')  # Field name made lowercase.
    profilenum = models.PositiveBigIntegerField(db_column='profileNum')  # Field name made lowercase.
    comment = models.CharField(max_length=100, blank=True, null=True)
    pick = models.CharField(max_length=10, blank=True, null=True)
    regtime = models.DateTimeField(db_column='regTime', blank=True, null=True)  # Field name made lowercase.
    cancel = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'audition_apply'


class AuditionInfo(models.Model):
    num = models.BigAutoField(primary_key=True)
    userid = models.CharField(db_column='userID', max_length=100)  # Field name made lowercase.
    title = models.CharField(max_length=100, blank=True, null=True)
    cate = models.CharField(max_length=50, blank=True, null=True)
    subcate = models.CharField(db_column='subCate', max_length=500, blank=True, null=True)  # Field name made lowercase.
    startdate = models.DateTimeField(db_column='startDate', blank=True, null=True)  # Field name made lowercase.
    enddate = models.DateTimeField(db_column='endDate', blank=True, null=True)  # Field name made lowercase.
    ordinary = models.CharField(max_length=100, blank=True, null=True)
    auditiondate = models.DateField(db_column='auditionDate', blank=True, null=True)  # Field name made lowercase.
    auditiontime = models.TimeField(db_column='auditionTime', blank=True, null=True)  # Field name made lowercase.
    each = models.CharField(max_length=10, blank=True, null=True)
    age = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=50, blank=True, null=True)
    career = models.CharField(max_length=50, blank=True, null=True)
    education = models.CharField(max_length=50, blank=True, null=True)
    image = models.CharField(max_length=1000, blank=True, null=True)
    essential = models.CharField(max_length=500, blank=True, null=True)
    preparation = models.TextField(blank=True, null=True)
    regtime = models.DateTimeField(db_column='regTime', blank=True, null=True)  # Field name made lowercase.
    updtime = models.DateTimeField(db_column='updTime', blank=True, null=True)  # Field name made lowercase.
    viewcount = models.IntegerField(db_column='viewCount', blank=True, null=True)  # Field name made lowercase.
    recommend = models.CharField(max_length=10, blank=True, null=True)
    recorder = models.PositiveIntegerField(db_column='recOrder', blank=True, null=True)  # Field name made lowercase.
    isdelete = models.CharField(db_column='isDelete', max_length=10, blank=True, null=True)  # Field name made lowercase.
    contenttype = models.CharField(db_column='contentType', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'audition_info'


class AuditionPick(models.Model):
    num = models.BigAutoField(primary_key=True)
    auditionnum = models.PositiveBigIntegerField(db_column='auditionNum')  # Field name made lowercase.
    userid = models.CharField(db_column='userID', max_length=100)  # Field name made lowercase.
    regtime = models.DateTimeField(db_column='regTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'audition_pick'


class AuditionView(models.Model):
    num = models.BigAutoField(primary_key=True)
    auditionnum = models.PositiveBigIntegerField(db_column='auditionNum')  # Field name made lowercase.
    userid = models.CharField(db_column='userID', max_length=100)  # Field name made lowercase.
    regtime = models.DateTimeField(db_column='regTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'audition_view'


class CateMain(models.Model):
    num = models.AutoField(primary_key=True)
    catecode = models.CharField(db_column='cateCode', unique=True, max_length=50)  # Field name made lowercase.
    catename = models.CharField(db_column='cateName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    cateorder = models.IntegerField(db_column='cateOrder', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cate_main'


class CateSub(models.Model):
    num = models.AutoField(primary_key=True)
    catecode = models.CharField(db_column='cateCode', max_length=50)  # Field name made lowercase.
    subcate = models.CharField(db_column='subCate', unique=True, max_length=50)  # Field name made lowercase.
    catename = models.CharField(db_column='cateName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    othergroup = models.CharField(db_column='otherGroup', max_length=100, blank=True, null=True)  # Field name made lowercase.
    cateorder = models.IntegerField(db_column='cateOrder', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cate_sub'


class EventBanner(models.Model):
    num = models.BigAutoField(primary_key=True)
    viewtype = models.CharField(db_column='viewType', max_length=50, blank=True, null=True)  # Field name made lowercase.
    position = models.CharField(max_length=50, blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    imagetype = models.CharField(db_column='imageType', max_length=50, blank=True, null=True)  # Field name made lowercase.
    mimage = models.CharField(db_column='mImage', max_length=200, blank=True, null=True)  # Field name made lowercase.
    wimage = models.CharField(db_column='wImage', max_length=200, blank=True, null=True)  # Field name made lowercase.
    nowview = models.CharField(db_column='nowView', max_length=10, blank=True, null=True)  # Field name made lowercase.
    clickcount = models.IntegerField(db_column='clickCount', blank=True, null=True)  # Field name made lowercase.
    regtime = models.DateTimeField(db_column='regTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'event_banner'


class ProfileCareer(models.Model):
    num = models.BigAutoField(primary_key=True)
    userid = models.CharField(db_column='userID', max_length=100)  # Field name made lowercase.
    profilenum = models.PositiveBigIntegerField(db_column='profileNum')  # Field name made lowercase.
    catetype = models.CharField(db_column='cateType', max_length=50, blank=True, null=True)  # Field name made lowercase.
    catesubtype = models.CharField(db_column='cateSubType', max_length=50, blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=100, blank=True, null=True)
    regtime = models.DateTimeField(db_column='regTime', blank=True, null=True)  # Field name made lowercase.
    updtime = models.DateTimeField(db_column='updTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'profile_career'


class ProfileComment(models.Model):
    num = models.BigAutoField(primary_key=True)
    profilenum = models.PositiveBigIntegerField(db_column='profileNum')  # Field name made lowercase.
    userid = models.CharField(db_column='userID', max_length=100)  # Field name made lowercase.
    content = models.CharField(max_length=500, blank=True, null=True)
    regtime = models.DateTimeField(db_column='regTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'profile_comment'


class ProfileEtccareer(models.Model):
    num = models.BigAutoField(primary_key=True)
    userid = models.CharField(db_column='userID', max_length=100)  # Field name made lowercase.
    profilenum = models.PositiveBigIntegerField(db_column='profileNum')  # Field name made lowercase.
    catetype = models.CharField(db_column='cateType', max_length=50, blank=True, null=True)  # Field name made lowercase.
    subcatetype = models.CharField(db_column='subCateType', max_length=50, blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=100, blank=True, null=True)
    regtime = models.DateTimeField(db_column='regTime', blank=True, null=True)  # Field name made lowercase.
    updtime = models.DateTimeField(db_column='updTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'profile_etccareer'


class ProfileInfo(models.Model):
    num = models.BigAutoField(primary_key=True)
    userid = models.CharField(db_column='userID', max_length=100)  # Field name made lowercase.
    profileimage = models.CharField(db_column='profileImage', max_length=500, blank=True, null=True)  # Field name made lowercase.
    detailimage = models.TextField(db_column='detailImage', blank=True, null=True)  # Field name made lowercase.
    artimage = models.TextField(db_column='artImage', blank=True, null=True)  # Field name made lowercase.
    height = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    weight = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    topsize = models.CharField(db_column='topSize', max_length=20, blank=True, null=True)  # Field name made lowercase.
    bottomsize = models.CharField(db_column='bottomSize', max_length=20, blank=True, null=True)  # Field name made lowercase.
    shoessize = models.IntegerField(db_column='shoesSize', blank=True, null=True)  # Field name made lowercase.
    skincolor = models.CharField(db_column='skinColor', max_length=50, blank=True, null=True)  # Field name made lowercase.
    haircolor = models.CharField(db_column='hairColor', max_length=50, blank=True, null=True)  # Field name made lowercase.
    foreign = models.CharField(max_length=500, blank=True, null=True)
    mainyoutube = models.CharField(db_column='mainYoutube', max_length=500, blank=True, null=True)  # Field name made lowercase.
    youtube = models.CharField(max_length=500, blank=True, null=True)
    talent = models.CharField(max_length=500, blank=True, null=True)
    comment = models.CharField(max_length=10000, blank=True, null=True)
    intercate = models.CharField(db_column='interCate', max_length=200, blank=True, null=True)  # Field name made lowercase.
    intersubcate = models.CharField(db_column='interSubCate', max_length=200, blank=True, null=True)  # Field name made lowercase.
    iscareer = models.CharField(db_column='isCareer', max_length=10, blank=True, null=True)  # Field name made lowercase.
    careeryear = models.CharField(db_column='careerYear', max_length=10, blank=True, null=True)  # Field name made lowercase.
    careermonth = models.CharField(db_column='careerMonth', max_length=10, blank=True, null=True)  # Field name made lowercase.
    regdate = models.DateTimeField(db_column='RegDate', blank=True, null=True)  # Field name made lowercase.
    viewcount = models.IntegerField(db_column='viewCount', blank=True, null=True)  # Field name made lowercase.
    cviewcount = models.IntegerField(db_column='cViewCount', blank=True, null=True)  # Field name made lowercase.
    pickcount = models.IntegerField(db_column='pickCount', blank=True, null=True)  # Field name made lowercase.
    public = models.CharField(max_length=10, blank=True, null=True)
    isdelete = models.CharField(db_column='isDelete', max_length=10, blank=True, null=True)  # Field name made lowercase.
    contenttype = models.CharField(db_column='contentType', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'profile_info'


class ProfilePick(models.Model):
    num = models.BigAutoField(primary_key=True)
    profilenum = models.PositiveBigIntegerField(db_column='profileNum')  # Field name made lowercase.
    userid = models.CharField(db_column='userID', max_length=100)  # Field name made lowercase.
    regtime = models.DateTimeField(db_column='regTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'profile_pick'


class ProfileShare(models.Model):
    num = models.BigIntegerField(primary_key=True)
    profilenum = models.PositiveBigIntegerField(db_column='profileNum')  # Field name made lowercase.
    userid = models.CharField(db_column='userID', max_length=100)  # Field name made lowercase.
    regtime = models.DateTimeField(db_column='regTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'profile_share'


class ProfileSuggest(models.Model):
    num = models.BigAutoField(primary_key=True)
    userid = models.CharField(db_column='userID', max_length=100)  # Field name made lowercase.
    suuserid = models.CharField(db_column='suUserID', max_length=100, blank=True, null=True)  # Field name made lowercase.
    profilenum = models.BigIntegerField(db_column='profileNum', blank=True, null=True)  # Field name made lowercase.
    auditionnum = models.PositiveBigIntegerField(db_column='auditionNum')  # Field name made lowercase.
    comment = models.TextField(blank=True, null=True)
    regtime = models.DateTimeField(db_column='regTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'profile_suggest'


class ProfileView(models.Model):
    num = models.BigAutoField(primary_key=True)
    profilenum = models.PositiveBigIntegerField(db_column='profileNum')  # Field name made lowercase.
    userid = models.CharField(db_column='userID', max_length=100)  # Field name made lowercase.
    regtime = models.DateTimeField(db_column='regTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'profile_view'


class ProfileViewCompany(models.Model):
    num = models.BigAutoField(primary_key=True)
    profilenum = models.PositiveBigIntegerField(db_column='profileNum')  # Field name made lowercase.
    userid = models.CharField(db_column='userID', max_length=100)  # Field name made lowercase.
    regtime = models.DateTimeField(db_column='regTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'profile_view_company'


class QaAdvertise(models.Model):
    num = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    content = models.CharField(max_length=500, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'qa_advertise'


class QaNotice(models.Model):
    num = models.BigAutoField(primary_key=True)
    userid = models.CharField(db_column='userID', max_length=100, blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(max_length=100, blank=True, null=True)
    content = models.CharField(max_length=10000, blank=True, null=True)
    image = models.CharField(max_length=500, blank=True, null=True)
    regdate = models.DateTimeField(db_column='regDate', blank=True, null=True)  # Field name made lowercase.
    contenttype = models.CharField(db_column='contentType', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'qa_notice'


class QaQanda(models.Model):
    num = models.BigAutoField(primary_key=True)
    userid = models.CharField(db_column='userID', max_length=100, blank=True, null=True)  # Field name made lowercase.
    cate = models.CharField(max_length=20, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    content = models.CharField(max_length=10000, blank=True, null=True)
    regdate = models.DateTimeField(db_column='regDate', blank=True, null=True)  # Field name made lowercase.
    contenttype = models.CharField(db_column='contentType', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'qa_qanda'


class QaQandaCate(models.Model):
    num = models.AutoField(primary_key=True)
    catecode = models.CharField(db_column='cateCode', unique=True, max_length=50)  # Field name made lowercase.
    catename = models.CharField(db_column='cateName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    cateorder = models.IntegerField(db_column='cateOrder', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'qa_qanda_cate'


class QaQandaComment(models.Model):
    num = models.BigAutoField(primary_key=True)
    qanum = models.PositiveBigIntegerField(db_column='qaNum')  # Field name made lowercase.
    userid = models.CharField(db_column='userID', max_length=100)  # Field name made lowercase.
    content = models.CharField(max_length=500, blank=True, null=True)
    regtime = models.DateTimeField(db_column='regTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'qa_qanda_comment'


class UserAgree(models.Model):
    num = models.AutoField(primary_key=True)
    savecolumn = models.CharField(db_column='saveColumn', max_length=50, blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(max_length=50, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
    use = models.CharField(max_length=10, blank=True, null=True)
    regdate = models.DateTimeField(db_column='regDate', blank=True, null=True)  # Field name made lowercase.
    upddate = models.DateTimeField(db_column='updDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user_agree'


class UserCompany(models.Model):
    num = models.BigAutoField(primary_key=True)
    userid = models.CharField(db_column='userID', max_length=100, blank=True, null=True)  # Field name made lowercase.
    logoimage = models.CharField(db_column='logoImage', max_length=200, blank=True, null=True)  # Field name made lowercase.
    licenseimage = models.CharField(db_column='licenseImage', max_length=200, blank=True, null=True)  # Field name made lowercase.
    artlicenseimage = models.CharField(db_column='artLicenseImage', max_length=200, blank=True, null=True)  # Field name made lowercase.
    license = models.CharField(max_length=200, blank=True, null=True)
    companyname = models.CharField(db_column='companyName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    addr1 = models.CharField(max_length=100, blank=True, null=True)
    addr2 = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    website = models.CharField(db_column='webSite', max_length=100, blank=True, null=True)  # Field name made lowercase.
    comment = models.CharField(max_length=10000, blank=True, null=True)
    regtime = models.DateTimeField(db_column='regTime', blank=True, null=True)  # Field name made lowercase.
    updtime = models.DateTimeField(db_column='updTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user_company'


class UserInfo(models.Model):
    num = models.BigAutoField(primary_key=True)
    userid = models.CharField(db_column='userID', unique=True, max_length=100)  # Field name made lowercase.
    password = models.CharField(max_length=100, blank=True, null=True)
    nickname = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    birth = models.CharField(max_length=10, blank=True, null=True)
    birthtype = models.CharField(db_column='birthType', max_length=10, blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(max_length=10, blank=True, null=True)
    nationality = models.CharField(max_length=10, blank=True, null=True)
    finalschool = models.CharField(db_column='finalSchool', max_length=50, blank=True, null=True)  # Field name made lowercase.
    school = models.CharField(max_length=50, blank=True, null=True)
    major = models.CharField(max_length=50, blank=True, null=True)
    entertain = models.CharField(max_length=100, blank=True, null=True)
    military = models.CharField(max_length=10, blank=True, null=True)
    zipcode = models.CharField(db_column='zipCode', max_length=10, blank=True, null=True)  # Field name made lowercase.
    addr1 = models.CharField(max_length=100, blank=True, null=True)
    addr2 = models.CharField(max_length=100, blank=True, null=True)
    instargram = models.CharField(max_length=200, blank=True, null=True)
    youtube = models.CharField(max_length=200, blank=True, null=True)
    agreeusage = models.CharField(db_column='agreeUsage', max_length=10, blank=True, null=True)  # Field name made lowercase.
    agreeprivacy = models.CharField(db_column='agreePrivacy', max_length=10, blank=True, null=True)  # Field name made lowercase.
    agreemarketing = models.CharField(db_column='agreeMarketing', max_length=10, blank=True, null=True)  # Field name made lowercase.
    agreeemail = models.CharField(db_column='agreeEmail', max_length=10, blank=True, null=True)  # Field name made lowercase.
    agreesms = models.CharField(db_column='agreeSms', max_length=10, blank=True, null=True)  # Field name made lowercase.
    jointype = models.CharField(db_column='joinType', max_length=20, blank=True, null=True)  # Field name made lowercase.
    regtime = models.DateTimeField(db_column='regTime', blank=True, null=True)  # Field name made lowercase.
    lastlogin = models.DateTimeField(db_column='lastLogin', blank=True, null=True)  # Field name made lowercase.
    logincount = models.IntegerField(db_column='loginCount', blank=True, null=True)  # Field name made lowercase.
    usertype = models.CharField(db_column='userType', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user_info'


class UserLogin(models.Model):
    num = models.BigAutoField(primary_key=True)
    userid = models.CharField(db_column='userID', max_length=100)  # Field name made lowercase.
    accesstime = models.DateTimeField(db_column='accessTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user_login'


class UserSearch(models.Model):
    num = models.BigAutoField(primary_key=True)
    userid = models.CharField(db_column='userID', max_length=100, blank=True, null=True)  # Field name made lowercase.
    search = models.CharField(max_length=200, blank=True, null=True)
    regdate = models.DateTimeField(db_column='regDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user_search'


class UserSms(models.Model):
    num = models.BigAutoField(primary_key=True)
    phonenum = models.CharField(db_column='phoneNum', max_length=20, blank=True, null=True)  # Field name made lowercase.
    certifier = models.CharField(max_length=10, blank=True, null=True)
    regdate = models.DateTimeField(db_column='regDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user_sms'
