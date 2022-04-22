
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('login/kakao/', views.kakao_login, name='kakao-login'), # 카카오 리다이렉트.
    path('login/kakao/callback/', views.kakao_login_callback, name='kakao-callback'), # 카카오 리다이렉트.
]