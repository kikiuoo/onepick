from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #path('', views.downstime, name='downstime'),
    path("ajax/updatePick/", views.updatePick, name="ajax-updatepick"),
    path("ajax/updateApplyPick/", views.updateApplyPick, name="ajax-updateApplyPick"),
    path("ajax/updateCounting/", views.updateCounting, name="ajax-updateCounting"),
    path("ajax/updateBannerCount/", views.updateBannerCount, name="ajax-updateBannerCount"),

    path("advertise/", views.advertise, name="advertisse"),
    path("advertise/callBack/", views.advertise_callBack, name="advertise-callback"),

    path("search/<search>/", views.searchList, name="searchList"),
    path("search/<search>/audi/<int:page>/", views.searchDetail_audi, name="searchDetail_audi"),
    path("search/<search>/profile/", views.searchDetail_pro, name="searchDetail_audi"),
    path("search/ajaxProfile/", views.getSearchProfile, name="getSearchProfile"),

    path("proList/<type>/<int:page>/<num>/<filter>/", views.proList, name="proList"),
    path("proList2/<type>/<int:page>/<num>/<filter>/", views.proList2, name="proList"),
    path("applyList/<num>/", views.applyList, name="applyList"),

    path(".well-known/pki-validation/gsdv.txt", views.gsdv, name="gsdv"),
    path(".sw.js", views.sw, name="sw"),

]