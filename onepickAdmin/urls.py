
from django.contrib import admin
from django.urls import path, include
from . import views
from . import viewsCs

urlpatterns = [
    path('', views.adminCheck, name='adminLoginCheck'),

    path('loginCheck/', views.adminLogin, name='adminLogin'),
    path('logout/', views.adminLogout, name='adminLogout'),

    path('cs/mail/', viewsCs.mailMain, name='mailMain'),
    path('cs/ajaxUserList/', viewsCs.ajaxUserList, name='ajaxUserList'),
    path('cs/summerImageUpload/', viewsCs.summerImageUpload, name='summerImageUpload'),
    path('cs/sendMail/', viewsCs.sendMail, name='sendMail'),
    path('cs/mailList/<int:page>/', viewsCs.mailList, name='mailList'),
    path('cs/mailDetail/<int:num>/', viewsCs.mailDetail, name='mailDetail'),

]