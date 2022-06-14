from django.core.files.storage import FileSystemStorage
from django.utils import timezone
import hashlib
import os
from django.conf import settings

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