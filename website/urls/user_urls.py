
from django.contrib import admin
from django.urls import path, include
from website.views import user_views as views

urlpatterns = [
    path('agreement/<int:num>/', views.agreement, name="user-agreement"),

    path('mypage/<type>/', views.userMypage, name="user-userMypage"),
    path('info/update/', views.updateUser, name="user-updateUser"),
    path('info/updateCallback/', views.updateCallback, name="user-updateCallback"),
    path('updatePW/', views.updatePW, name="user-updatePW"),
    path('ajax/updatePWCallback/', views.updatePWCallback, name="user-updatePWCallback"),

    path('quit/', views.quit, name="user-quit"),
    path('quitCallback/', views.quitCallback, name="user-quitCallback"),

    path('ajax/findOldUser/', views.ajax_findOldUser, name="user-ajax-findOldUser"),
    path('ajax/findUser/', views.ajax_findUser, name="user-ajax-findUser"),
    path('ajax/pwPhoneComfirm/', views.ajax_pwPhoneComfirm, name="user-ajax-pwPhoneComfirm"),
    path('ajax/phoneComfirm/', views.ajax_phoneComfirm, name="user-ajax-phoneComfirm"),
    path('ajax/checkConfirm/', views.ajax_checkConfirm, name="user-ajax-checkConfirm"),

]