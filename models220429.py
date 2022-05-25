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
    auditionnum = models.ForeignKey('AuditionInfo', models.DO_NOTHING, db_column='auditionNum')  # Field name made lowercase.
    profilenum = models.ForeignKey('ProfileInfo', models.DO_NOTHING, db_column='profileNum')  # Field name made lowercase.
    comment = models.CharField(max_length=100, blank=True, null=True)
    pick = models.CharField(max_length=10, blank=True, null=True)
    regtime = models.DateTimeField(db_column='regTime', blank=True, null=True)  # Field name made lowercase.
    cancel = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'audition_apply'


class AuditionInfo(models.Model):
    num = models.BigAutoField(primary_key=True)
    userid = models.ForeignKey('UserInfo', models.DO_NOTHING, db_column='userID')  # Field name made lowercase.
    cate = models.ForeignKey('CateMain', models.DO_NOTHING, db_column='cate', blank=True, null=True)
    subcate = models.CharField(db_column='subCate', max_length=100, blank=True, null=True)  # Field name made lowercase.
    startdate = models.DateTimeField(db_column='startDate', blank=True, null=True)  # Field name made lowercase.
    enddate = models.DateTimeField(db_column='endDate', blank=True, null=True)  # Field name made lowercase.
    ordinary = models.CharField(max_length=10, blank=True, null=True)
    auditiondate = models.DateField(db_column='auditionDate', blank=True, null=True)  # Field name made lowercase.
    auditiontime = models.TimeField(db_column='auditionTime', blank=True, null=True)  # Field name made lowercase.
    each = models.CharField(max_length=10, blank=True, null=True)
    age = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=50, blank=True, null=True)
    career = models.CharField(max_length=50, blank=True, null=True)
    education = models.CharField(max_length=50, blank=True, null=True)
    image = models.CharField(max_length=200, blank=True, null=True)
    essential = models.CharField(max_length=500, blank=True, null=True)
    field_preparation = models.CharField(db_column='\tpreparation', max_length=500, blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    regtime = models.DateTimeField(db_column='regTime', blank=True, null=True)  # Field name made lowercase.
    updtime = models.DateTimeField(db_column='updTime', blank=True, null=True)  # Field name made lowercase.
    viewcount = models.IntegerField(db_column='viewCount', blank=True, null=True)  # Field name made lowercase.
    recommend = models.CharField(max_length=10, blank=True, null=True)
    recorder = models.IntegerField(db_column='recOrder', blank=True, null=True)  # Field name made lowercase.
    isdelete = models.CharField(db_column='isDelete', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'audition_info'


class AuditionPick(models.Model):
    num = models.BigIntegerField(primary_key=True)
    auditionnum = models.ForeignKey(AuditionInfo, models.DO_NOTHING, db_column='auditionNum')  # Field name made lowercase.
    userid = models.ForeignKey('UserInfo', models.DO_NOTHING, db_column='userID')  # Field name made lowercase.
    regtime = models.DateTimeField(db_column='regTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'audition_pick'


class AuditionView(models.Model):
    num = models.BigIntegerField(primary_key=True)
    auditionnum = models.ForeignKey(AuditionInfo, models.DO_NOTHING, db_column='auditionNum')  # Field name made lowercase.
    userid = models.ForeignKey('UserInfo', models.DO_NOTHING, db_column='userID')  # Field name made lowercase.
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
    catecode = models.ForeignKey(CateMain, models.DO_NOTHING, db_column='cateCode')  # Field name made lowercase.
    subcate = models.CharField(db_column='subCate', unique=True, max_length=50)  # Field name made lowercase.
    catename = models.CharField(db_column='cateName', max_length=100, blank=True, null=True)  # Field name made lowercase.
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
    userid = models.ForeignKey('UserInfo', models.DO_NOTHING, db_column='userID')  # Field name made lowercase.
    profilenum = models.ForeignKey('ProfileInfo', models.DO_NOTHING, db_column='profileNum')  # Field name made lowercase.
    catetype = models.IntegerField(db_column='cateType', blank=True, null=True)  # Field name made lowercase.
    catesubtype = models.IntegerField(db_column='cateSubType', blank=True, null=True)  # Field name made lowercase.
    content = models.CharField(max_length=100, blank=True, null=True)
    regtime = models.DateTimeField(db_column='regTime', blank=True, null=True)  # Field name made lowercase.
    updtime = models.DateTimeField(db_column='updTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'profile_career'


class ProfileComment(models.Model):
    num = models.BigIntegerField(primary_key=True)
    profilenum = models.ForeignKey('ProfileInfo', models.DO_NOTHING, db_column='profileNum')  # Field name made lowercase.
    userid = models.ForeignKey('UserInfo', models.DO_NOTHING, db_column='userID')  # Field name made lowercase.
    content = models.CharField(max_length=500, blank=True, null=True)
    regtime = models.DateTimeField(db_column='regTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'profile_comment'


class ProfileEtccareer(models.Model):
    num = models.BigAutoField(primary_key=True)
    userid = models.ForeignKey('UserInfo', models.DO_NOTHING, db_column='userID')  # Field name made lowercase.
    profilenum = models.ForeignKey('ProfileInfo', models.DO_NOTHING, db_column='profileNum')  # Field name made lowercase.
    catetype = models.IntegerField(db_column='cateType', blank=True, null=True)  # Field name made lowercase.
    subcatetype = models.IntegerField(db_column='subCateType', blank=True, null=True)  # Field name made lowercase.
    content = models.CharField(max_length=100, blank=True, null=True)
    regtime = models.DateTimeField(db_column='regTime', blank=True, null=True)  # Field name made lowercase.
    updtime = models.DateTimeField(db_column='updTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'profile_etccareer'


class ProfileInfo(models.Model):
    num = models.BigAutoField(primary_key=True)
    userid = models.ForeignKey('UserInfo', models.DO_NOTHING, db_column='userID')  # Field name made lowercase.
    profileimage = models.CharField(db_column='profileImage', max_length=500, blank=True, null=True)  # Field name made lowercase.
    detailimage = models.TextField(db_column='detailImage', blank=True, null=True)  # Field name made lowercase.
    height = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    weight = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    topsize = models.CharField(db_column='topSize', max_length=20, blank=True, null=True)  # Field name made lowercase.
    bottomsize = models.IntegerField(db_column='bottomSize', blank=True, null=True)  # Field name made lowercase.
    shoessize = models.IntegerField(db_column='shoesSize', blank=True, null=True)  # Field name made lowercase.
    skincolor = models.CharField(db_column='skinColor', max_length=50, blank=True, null=True)  # Field name made lowercase.
    haircolor = models.CharField(db_column='hairColor', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sns = models.CharField(max_length=500, blank=True, null=True)
    license = models.CharField(max_length=500, blank=True, null=True)
    foreign = models.CharField(max_length=500, blank=True, null=True)
    youtube = models.CharField(max_length=500, blank=True, null=True)
    linecomment = models.CharField(db_column='lineComment', max_length=100, blank=True, null=True)  # Field name made lowercase.
    intercate = models.CharField(db_column='interCate', max_length=50, blank=True, null=True)  # Field name made lowercase.
    intersubcate = models.CharField(db_column='interSubCate', max_length=50, blank=True, null=True)  # Field name made lowercase.
    regdate = models.DateTimeField(db_column='RegDate', blank=True, null=True)  # Field name made lowercase.
    viewcount = models.IntegerField(db_column='viewCount', blank=True, null=True)  # Field name made lowercase.
    public = models.CharField(max_length=10, blank=True, null=True)
    isdelete = models.CharField(db_column='isDelete', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'profile_info'


class ProfilePick(models.Model):
    num = models.BigIntegerField(primary_key=True)
    profilenum = models.ForeignKey(ProfileInfo, models.DO_NOTHING, db_column='profileNum')  # Field name made lowercase.
    userid = models.ForeignKey('UserInfo', models.DO_NOTHING, db_column='userID')  # Field name made lowercase.
    regtime = models.DateTimeField(db_column='regTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'profile_pick'


class ProfileShare(models.Model):
    num = models.BigIntegerField(primary_key=True)
    profilenum = models.ForeignKey(ProfileInfo, models.DO_NOTHING, db_column='profileNum')  # Field name made lowercase.
    userid = models.ForeignKey('UserInfo', models.DO_NOTHING, db_column='userID')  # Field name made lowercase.
    regtime = models.DateTimeField(db_column='regTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'profile_share'


class ProfileSuggest(models.Model):
    num = models.BigAutoField(primary_key=True)
    userid = models.ForeignKey('UserInfo', models.DO_NOTHING, db_column='userID')  # Field name made lowercase.
    auditionnum = models.PositiveBigIntegerField(db_column='auditionNum')  # Field name made lowercase.
    comment = models.CharField(max_length=500, blank=True, null=True)
    regtime = models.DateTimeField(db_column='regTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'profile_suggest'


class ProfileView(models.Model):
    num = models.BigIntegerField(primary_key=True)
    profilenum = models.ForeignKey(ProfileInfo, models.DO_NOTHING, db_column='profileNum')  # Field name made lowercase.
    userid = models.ForeignKey('UserInfo', models.DO_NOTHING, db_column='userID')  # Field name made lowercase.
    regtime = models.DateTimeField(db_column='regTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'profile_view'


class UserCompany(models.Model):
    num = models.PositiveBigIntegerField(primary_key=True)
    userid = models.ForeignKey('UserInfo', models.DO_NOTHING, db_column='userID', blank=True, null=True)  # Field name made lowercase.
    logoimage = models.CharField(db_column='logoImage', max_length=200, blank=True, null=True)  # Field name made lowercase.
    license = models.CharField(max_length=200, blank=True, null=True)
    companyname = models.CharField(db_column='companyName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    addr1 = models.CharField(max_length=100, blank=True, null=True)
    addr2 = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    website = models.CharField(db_column='webSite', max_length=100, blank=True, null=True)  # Field name made lowercase.
    comment = models.CharField(max_length=200, blank=True, null=True)
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
    school = models.CharField(max_length=50, blank=True, null=True)
    agreeusage = models.CharField(db_column='agreeUsage', max_length=10, blank=True, null=True)  # Field name made lowercase.
    agreeprivacy = models.CharField(db_column='agreePrivacy', max_length=10, blank=True, null=True)  # Field name made lowercase.
    agreemarketing = models.CharField(db_column='agreeMarketing', max_length=10, blank=True, null=True)  # Field name made lowercase.
    agreeemail = models.CharField(db_column='agreeEmail', max_length=10, blank=True, null=True)  # Field name made lowercase.
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
    userid = models.ForeignKey(UserInfo, models.DO_NOTHING, db_column='userID')  # Field name made lowercase.
    accesstime = models.DateTimeField(db_column='accessTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user_login'