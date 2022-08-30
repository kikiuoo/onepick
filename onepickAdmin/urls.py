
from django.contrib import admin
from django.urls import path, include
from . import views
from . import viewsCs
from . import viewsNotice
from . import viewsUser
from . import viewsProfile

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
    path('user/excel/<type>/<word>/', viewsUser.excel, name='excel'),
    path('user/logList/<int:page>/', viewsUser.logList, name='logList'),

    # Profile url
    path('profile/list/<type>/<int:page>/', viewsProfile.list, name='list'),
    path('profile/listSearch/<type>/<word>/<int:page>/', viewsProfile.listSearch, name='listSearch'),



    path('cs/mail/', viewsCs.mailMain, name='mailMain'),
    path('cs/ajaxUserList/', viewsCs.ajaxUserList, name='ajaxUserList'),
    path('cs/summerImageUpload/', viewsCs.summerImageUpload, name='summerImageUpload'),
    path('cs/sendMail/', viewsCs.sendMail, name='sendMail'),
    path('cs/mailList/<int:page>/', viewsCs.mailList, name='mailList'),
    path('cs/mailDetail/<int:num>/', viewsCs.mailDetail, name='mailDetail'),

]