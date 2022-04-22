from django.contrib.sites import requests
from django.shortcuts import render, redirect
from user.exception import *
from user.models import *
import os

# Create your views here.
def kakao_login(request):
    if request.user.is_authenticated:
        raise SocialLoginException("User already logged in")
    client_id = "12d0c003da263dba9fcabe8d20c36045"
    redirect_uri = "http://ksnpick.com/users/login/kakao/callback/"

    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )

def kakao_login_callback(request):
    if request.user.is_authenticated:
        raise SocialLoginException("User already logged in")
    code = request.GET.get("code", None)
    if code is None:
        KakaoException("Can't get code")
    client_id = "12d0c003da263dba9fcabe8d20c36045"
    redirect_uri = "http://ksnpick.com/users/login/kakao/callback/"
    client_secret = os.environ.get("KAKAO_SECRET")
    request_access_token = requests.post(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}&client_secret={client_secret}",
        headers={"Accept": "application/json"},
    )
    access_token_json = request_access_token.json()
    error = access_token_json.get("error", None)
    if error is not None:
        print(error)
        KakaoException("Can't get access token")
    access_token = access_token_json.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    profile_request = requests.post(
        "https://kapi.kakao.com/v2/user/me",
        headers=headers,
    )
    profile_json = profile_request.json()
    kakao_account = profile_json.get("kakao_account")
    profile = kakao_account.get("profile")

    nickname = profile.get("nickname", None)
    email = kakao_account.get("email", None)
    gender = kakao_account.get("gender", None)

    return redirect(request, "picktalk/index.html")
