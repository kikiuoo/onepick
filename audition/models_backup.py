from datetime import datetime

from django.db import models

# Create your models here.
from myonepick.common import NO_PERIOD
from user.models import User, GENDER, NORMAL, COMPANY


class AuditionCategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=300, null=True, blank=True)

    regTime = models.DateTimeField(auto_now_add=True)
    updTime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name if self.name else str(self.id)

    def store(self):
        self.save()
        return self


class AuditionSubCategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=300, null=True, blank=True)
    category = models.ForeignKey(AuditionCategory, related_name='subCategories', null=True, blank=True, on_delete=models.SET_NULL)

    regTime = models.DateTimeField(auto_now_add=True)
    updTime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (self.category.__str__() if self.category else '') + self.name if self.name else str(self.id)

    def store(self):
        self.save()
        return self

    def get_category_id(self):
        return self.category_id if self.category else 0

    def get_category_name(self):
        return self.category.name if self.category else 0


class AuditionImages(models.Model):
    id = models.BigAutoField(primary_key=True)
    image = models.ImageField(upload_to='photos/audition/image', null=True, blank=True)

    regTime = models.DateTimeField(auto_now_add=True)
    updTime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.image.url) if self.image else str(self.id)

    def store(self, name, photo):
        self.image.save(name, photo)
        self.save()
        return self

    def get_url(self):
        return str(self.image.url) if self.image else str(self.id)


class Audition(models.Model):
    id = models.BigAutoField(primary_key=True)
    register = models.ForeignKey(User, related_name='myAuditions', blank=True, null=True, on_delete=models.SET_NULL)

    logoImage = models.ImageField(upload_to='photos/audition/logo', null=True, blank=True)
    otherImages = models.ManyToManyField(AuditionImages, null=True)
    webUrl = models.CharField(max_length=500, null=True, blank=True)
    title = models.CharField(max_length=500, null=True, blank=True)
    subCategories = models.ManyToManyField(AuditionSubCategory, null=True)
    startDate = models.DateTimeField(null=True, blank=True)
    endDate = models.DateTimeField(null=True, blank=True)
    isNoPeriod = models.BooleanField(default=False)
    auditionDate = models.DateField(null=True, blank=True)
    auditionTime = models.TimeField(null=True, blank=True)
    age = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=100, choices=GENDER, null=True, blank=True)
    career = models.CharField(max_length=300, null=True, blank=True)
    required = models.CharField(max_length=500, null=True, blank=True)
    prepared = models.CharField(max_length=500, null=True, blank=True)

    email = models.CharField(max_length=150, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)

    regTime = models.DateTimeField(auto_now_add=True)
    updTime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title) if self.title else str(self.id)

    def store(self):
        self.save()
        return self

    def get_start_date(self):
        return NO_PERIOD if self.isNoPeriod else (self.startDate.strftime('%Y-%m-%d') if self.startDate else '')

    def get_end_date(self):
        return NO_PERIOD if self.isNoPeriod else (self.endDate.strftime('%Y-%m-%d') if self.endDate else '')

    def get_other_images(self):
        return [oi.get_url() for oi in self.otherImages.order_by('regTime')]

    def get_remain_date(self):
        if not self.endDate:
            return ''
        today = datetime.now().date()
        remainDate = (self.endDate.date() - today).days
        return (str(remainDate) + '일전') if remainDate > 0 else '오늘 마감'