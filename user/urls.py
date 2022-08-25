
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('login/kakao/', views.kakao_login, name='kakao-login'), # 카카오 리다이렉트.
    path('login/kakao/callback/', views.kakao_login_callback, name='kakao-callback'), # 카카오 리다이렉트.

    path('login/google/', views.googleLogin, name='google-login'),  # 구글 리다이렉트.
    path('login/google/callback/', views.googleLoginCallback, name='google-callback'),  # 구글 리다이렉트.

    path('login/naver/', views.naver_login, name='apple-login'),  # 애플 리다이렉트.
    path('login/naver/callback/', views.naver_login_callback, name='apple-callback'),  # 애플 리다이렉트.

    path('login/local/', views.localLogin, name='local-login'), # 로컬 로그인.
    path('login/logincallback/', views.localLoginCallback, name='local-logincallback'), # 로컬 로그인.
    path('logout/local/', views.locallogout, name='local-logout'), # 로컬 로그아웃.

    path('findUser/', views.finduser, name='local-finduser'),
    path('findPW/', views.findPW, name='local-findPW'),
    path('updatePW/', views.updatePW, name='local-updatePW'),


    path('join/<userID>/<type>/', views.join, name='joins'),
    path('joins/updateUser/', views.joinUpdate, name="join-update"),
    path('joinView/', views.joinView, name='joinView'),

    path('agreement/<int:num>/', views.agreement, name="user-agreement"),

    path('mypage/<type>/', views.userMypage, name="user-userMypage"),
    path('info/update/', views.updateUser, name="user-updateUser"),
    path('info/updateCallback/', views.updateCallback, name="user-updateCallback"),
    path('updatePW/', views.updatePW, name="user-updatePW"),
    path('ajax/updatePWCallback/', views.updatePWCallback, name="user-updatePWCallback"),

    path('ajax/findOldUser/', views.ajax_findOldUser, name="user-ajax-findOldUser"),
    path('ajax/findUser/', views.ajax_findUser, name="user-ajax-findUser"),
    path('ajax/pwPhoneComfirm/', views.ajax_pwPhoneComfirm, name="user-ajax-pwPhoneComfirm"),
    path('ajax/phoneComfirm/', views.ajax_phoneComfirm, name="user-ajax-phoneComfirm"),
    path('ajax/checkConfirm/', views.ajax_checkConfirm, name="user-ajax-checkConfirm"),

]