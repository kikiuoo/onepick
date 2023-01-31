
from django.contrib import admin
from django.urls import path, include
from website.views import login_views as views

urlpatterns = [
    path('kakao/', views.kakao_login, name='kakao-login'), # 카카오 리다이렉트.
    path('kakao/callback/', views.kakao_login_callback, name='kakao-callback'), # 카카오 리다이렉트.

    path('google/', views.googleLogin, name='google-login'),  # 구글 리다이렉트.
    path('google/callback/', views.googleLoginCallback, name='google-callback'),  # 구글 리다이렉트.

    path('naver/', views.naver_login, name='apple-login'),  # 애플 리다이렉트.
    path('naver/callback/', views.naver_login_callback, name='apple-callback'),  # 애플 리다이렉트.

    path('local/', views.localLogin, name='local-login'), # 로컬 로그인.
    path('logincallback/', views.localLoginCallback, name='local-logincallback'), # 로컬 로그인.
    path('logout/local/', views.locallogout, name='local-logout'), # 로컬 로그아웃.

    path('findUser/', views.finduser, name='local-finduser'),
    path('findPW/', views.findPW, name='local-findPW'),
    path('updatePW_local/', views.updatePW_local, name='local-updatePW_local'),

    path('join/<userID>/<type>/', views.join, name='joins'),
    path('joins/updateUser/', views.joinUpdate, name="join-update"),
    path('socialAgree/<userID>/', views.socialAgree, name='socialAgree'),
    path('joinSocial/<userID>/', views.joinSocial, name='joinSocial'),

    path('joinView/', views.joinView, name='joinView'),
    path('joinAgreement_c/', views.joinAgreementC, name='joinAgreement_c'),

    path('joinCompany/', views.joinCompany, name='joinCompany'),
    path('joinCompanyCallback/', views.joinCompanyCallback, name='joinCompanyCallback'),
    path('joinUser/', views.joinUser, name='joinUser'),
    path('joinUserCallback/', views.joinUserCallback, name='joinUserCallback'),

    path('ajax/findOldUser/', views.ajax_findOldUser, name="user-ajax-findOldUser"),
    path('ajax/findUser/', views.ajax_findUser, name="user-ajax-findUser"),
    path('ajax/idFindPhoneComfirm/', views.ajax_idFindPhoneComfirm, name="user-ajax-idFindPhoneComfirm"),
    path('ajax/pwPhoneComfirm/', views.ajax_pwPhoneComfirm, name="user-ajax-pwPhoneComfirm"),
    path('ajax/phoneComfirm/', views.ajax_phoneComfirm, name="user-ajax-phoneComfirm"),
    path('ajax/checkConfirm/', views.ajax_checkConfirm, name="user-ajax-checkConfirm"),
    path('ajax/checkOverlapID/', views.ajax_checkOverlapID, name="user-ajax-checkOverlapID"),

]