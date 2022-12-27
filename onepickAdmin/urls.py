
from django.contrib import admin
from django.urls import path, include
from . import views
from . import viewsCs
from . import viewsNotice
from . import viewsUser
from . import viewsProfile
from . import viewsAudi
from . import viewsDisplay
from . import viewsClass

urlpatterns = [
    path('', views.adminCheck, name='adminLoginCheck'),

    #main url
    path('loginCheck/', views.adminLogin, name='adminLogin'),
    path('logout/', views.adminLogout, name='adminLogout'),
    path('ajax/getGraph/', views.ajaxGetGraph, name='ajaxGetGraph'),

    # notice Url
    path('notice/list/<type>/<int:page>/', viewsNotice.list, name='list'),
    path('notice/write/', viewsNotice.write, name='write'),
    path('notice/writeCallBack/', viewsNotice.writeCallBack, name='writeCallBack'),
    path('notice/viewer/<int:num>/', viewsNotice.viewer, name='viewer'),
    path('notice/edit/<int:num>/', viewsNotice.edit, name='edit'),
    path('notice/editCallBack/', viewsNotice.editCallBack, name='editCallBack'),
    path('notice/summerImageUpload/', viewsNotice.summerImageUpload, name='summerImageUpload'),
    path('notice/delete/<int:num>/', viewsNotice.delete, name='delete'),

    # User url
    path('user/list/<type>/<int:page>/', viewsUser.list, name='list'),
    path('user/listSearch/<type>/<word>/<int:page>/', viewsUser.listSearch, name='listSearch'),
    path('user/edit/<int:num>/', viewsUser.edit, name='edit'),
    path('user/editCallback/', viewsUser.editCallback, name='editCallback'),
    path('user/updateComany/', viewsUser.updateComany, name='updateComany'),
    path('user/addCompany/', viewsUser.addCompany, name='addCompany'),
    path('user/excel/<type>/<word>/', viewsUser.excel, name='excel'),
    path('user/logList/<int:page>/', viewsUser.logList, name='logList'),

    # Profile url
    path('profile/list/<type>/<int:page>/', viewsProfile.list, name='list'),
    path('profile/listSearch/<type>/<word>/<int:page>/', viewsProfile.listSearch, name='listSearch'),
    path('profile/saveRecommendProfile/', viewsProfile.saveRecommendProfile, name='saveRecommendProfile'),

    # audition url
    path('audi/list/<type>/<int:page>/', viewsAudi.list, name='list'),
    path('audi/listSearch/<type>/<word>/<int:page>/', viewsAudi.listSearch, name='listSearch'),
    path('audi/saveRecommendAudi/', viewsAudi.saveRecommendAudi, name='saveRecommendAudi'),

    # display url
    path('display/audi/', viewsDisplay.audiList, name='audiList'),
    path('display/audi/findAudition/', viewsDisplay.findAudition, name='findAudition'),
    path('display/audi/saveRecommend/', viewsDisplay.saveRecommend, name='saveRecommend'),
    path('display/audi/updateOrder/', viewsDisplay.updateOrder, name='updateOrder'),

    path('display/profile/', viewsDisplay.proList, name='proList'),
    path('display/profile/findProfile/', viewsDisplay.findProfile, name='findProfile'),
    path('display/profile/saveRecommend/', viewsDisplay.proSaveRecommend, name='proSaveRecommend'),

    path('display/banner/', viewsDisplay.bannerList, name='bannerList'),
    path('display/banner/write/', viewsDisplay.bannerWrite, name='bannerWrite'),
    path('display/banner/writeCallback/', viewsDisplay.writeCallback, name='writeCallback'),
    path('display/banner/edit/<int:num>/', viewsDisplay.bannerEdit, name='bannerEdit'),
    path('display/banner/editCallback/', viewsDisplay.editCallback, name='editCallback'),
    path('display/banner/delete/<int:num>/', viewsDisplay.bannerDelete, name='bannerDelete'),

    path('display/popup/', viewsDisplay.popupList, name='popupList'),
    path('display/popup/write/', viewsDisplay.popupWrite, name='popupWrite'),
    path('display/popup/writeCallback/', viewsDisplay.popupWriteCallback, name='popupWriteCallback'),
    path('display/popup/edit/<int:num>/', viewsDisplay.popupEdit, name='popupEdit'),
    path('display/popup/editCallback/', viewsDisplay.popupEditCallback, name='popupEditCallback'),
    path('display/popup/delete/<int:num>/', viewsDisplay.popupDelete, name='popupDelete'),

    # cs url
    path('cs/qanda/', viewsCs.qandaList, name='qandaList'),
    path('cs/mail/', viewsCs.mailMain, name='mailMain'),
    path('cs/ajaxUserList/', viewsCs.ajaxUserList, name='ajaxUserList'),
    path('cs/summerImageUpload/', viewsCs.summerImageUpload, name='summerImageUpload'),
    path('cs/sendMail/', viewsCs.sendMail, name='sendMail'),
    path('cs/mailList/<int:page>/', viewsCs.mailList, name='mailList'),
    path('cs/mailDetail/<int:num>/', viewsCs.mailDetail, name='mailDetail'),
    path('cs/youtube/', viewsCs.youtube, name='youtube'),
    path('cs/checkYoutube/', viewsCs.checkYoutube, name='checkYoutube'),

    # classfy url
    path('classfy/', viewsClass.classfy, name='classfy'),
    path('classfy/saveClassfy/', viewsClass.saveClassfy, name='saveClassfy'),

]