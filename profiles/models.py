from django.db import models

# Create your models here.
from django.db.models import Sum, Max

from audition.models import AuditionCategory, AuditionSubCategory, Audition
from myonepick.common import NORMAL, COMPANY
from user.models import User, GENDER

TOP_SIZE = [
    ('XXS', 'XXS'),
    ('XS', 'XS'),
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
    ('2XL', '2XL'),
    ('3XL', '3XL'),
]

APPLY_TYPE = [
    ('배우', '배우'),
    ('모델', '모델'),
    ('가수', '가수'),
    ('댄서', '댄서'),
    ('인플루언서', '인플루언서'),
]

EXTRA_APPLY_SUB_TYPE = [
    ('아르바이트', '아르바이트'),
    ('취업', '취업'),
    ('기타', '기타'),
]


class ApplySubType(models.Model):
    id = models.BigAutoField(primary_key=True)
    applyType = models.ForeignKey(AuditionCategory, null=True, blank=True, on_delete=models.SET_NULL)
    applySubType = models.ForeignKey(AuditionSubCategory, null=True, blank=True, on_delete=models.SET_NULL)

    regTime = models.DateTimeField(auto_now_add=True)
    updTime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.applySubType.__str__() if self.applySubType else str(self.id)

    def store(self):
        self.save()
        return self


class ProfileImage(models.Model):
    id = models.BigAutoField(primary_key=True)
    image = models.ImageField(upload_to='photos/profile/additional', null=True, blank=True)

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


NOT_REQUIRED_FIELDS = [
            'topSize',
            'bottomSize',
            'footSize',
            'skinColor',
            'hairColor'
        ]


class Profile(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, related_name='profiles', blank=True, null=True, on_delete=models.SET_NULL)

    mainImage = models.ImageField(upload_to='photos/profiles/main', null=True, blank=True)
    otherImages = models.ManyToManyField(ProfileImage, null=True)

    name = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    school = models.CharField(max_length=200, null=True, blank=True)
    snsUrl = models.CharField(max_length=500, null=True, blank=True)
    language = models.CharField(max_length=500, null=True, blank=True)
    youtubeUrl = models.CharField(max_length=500, null=True, blank=True)
    youtubeId = models.CharField(max_length=100, null=True, blank=True)

    height = models.CharField(max_length=100, null=True, blank=True)
    weight = models.CharField(max_length=100, null=True, blank=True)

    topSize = models.CharField(max_length=50, choices=TOP_SIZE, null=True, blank=True)
    bottomSize = models.CharField(max_length=100, null=True, blank=True)
    footSize = models.CharField(max_length=100, null=True, blank=True)
    skinColor = models.CharField(max_length=100, null=True, blank=True)
    hairColor = models.CharField(max_length=100, null=True, blank=True)

    oneSentence = models.CharField(max_length=500, null=True, blank=True)
    introduction = models.TextField(max_length=5000, null=True, blank=True)

    representImage = models.ImageField(upload_to='photos/profile/represent', null=True, blank=True)

    isDefault = models.BooleanField(default=True)

    regTime = models.DateTimeField(auto_now_add=True)
    updTime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.__str__() if self.user else str(self.id)

    def store(self):
        self.save()
        return self

    def get_secret_name(self):
        if not self.name:
            return ''
        return self.name[:-2] + '*' + self.name[-1:]

    def get_career(self):
        applies = set()
        careers = {}
        for career in self.careers.values('applySubType').annotate(name=Max('applySubType__applyType__name')).values('name', 'contents').order_by('-regTime'):
            name = career['name']
            if name:
                applies.add(name)
            contents = career.get('contents', '')
            if not careers.get(name, None):
                careers[name] = []
            careers[name].append(contents)

        return {
            'applies': ' '.join(list(applies)),
            'careers': careers
        }

    def get_other_images(self):
        return [img.get_url() for img in self.otherImages.order_by('-regTime')]

    def get_complete_rate(self):
        totalPoint = self.otherImages.count() * 5 + \
                     (5 if self.youtubeUrl else 0) + \
                     (5 if self.height or self.weight else 0) + \
                     (5 if self.phone else 0)

        for nrf in NOT_REQUIRED_FIELDS:
            if getattr(self, nrf) is not None:
                totalPoint += 5

        return totalPoint if totalPoint <= 100 else 100


class Career(models.Model):
    id = models.BigAutoField(primary_key=True)
    profile = models.ForeignKey(Profile, related_name='careers', blank=True, null=True, on_delete=models.SET_NULL)
    applySubType = models.ForeignKey(ApplySubType, blank=True, null=True, on_delete=models.SET_NULL)
    contents = models.CharField(max_length=3000, null=True, blank=True)

    regTime = models.DateTimeField(auto_now_add=True)
    updTime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.contents if self.contents else str(self.id)

    def store(self):
        self.save()
        return self


class License(models.Model):
    id = models.BigAutoField(primary_key=True)
    profile = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.SET_NULL)
    contents = models.CharField(max_length=300, null=True, blank=True)

    regTime = models.DateTimeField(auto_now_add=True)
    updTime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.contents if self.contents else str(self.id)

    def store(self):
        self.save()
        return self



# class Language(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     profile = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.SET_NULL)
#     language = models.CharField(max_length=300, null=True, blank=True)
#     level = models.CharField(max_length=300, null=True, blank=True)
#
#     regTime = models.DateTimeField(auto_now_add=True)
#     updTime = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.language if self.language else str(self.id)
#
#     def store(self):
#         self.save()
#         return self