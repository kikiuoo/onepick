from django.urls import path
from website.views import search_views as views

urlpatterns = [
    path("<search>/", views.searchList, name="searchList"),
    path("<search>/audi/<int:page>/", views.searchDetail_audi, name="searchDetail_audi"),
    path("<search>/profile/", views.searchDetail_pro, name="searchDetail_audi"),
    path("ajaxProfile/", views.getSearchProfile, name="getSearchProfile"),
]