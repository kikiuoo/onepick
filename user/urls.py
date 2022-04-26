
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('login/kakao/', views.kakao_login, name='kakao-login'), # 카카오 리다이렉트.
    path('login/kakao/callback/', views.kakao_login_callback, name='kakao-callback'), # 카카오 리다이렉트.

    path('login/google/', views.googleLogin, name='google-login'),  # 구글 리다이렉트.
    path('login/google/callback/', views.googleLoginCallback, name='google-callback'),  # 구글 리다이렉트.

    path('login/local/', views.localLogin, name='local-login'), # 로컬 로그인.
    path('logout/local/', views.locallogout, name='local-logout'), # 로컬 로그아웃.

]