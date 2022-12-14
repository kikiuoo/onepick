from django.urls import path
from website.views import common_views as views

urlpatterns = [

    path("updatePick/", views.updatePick, name="ajax-updatepick"),
    path("updateApplyPick/", views.updateApplyPick, name="ajax-updateApplyPick"),
    path("updateCounting/", views.updateCounting, name="ajax-updateCounting"),
    path("updateBannerCount/", views.updateBannerCount, name="ajax-updateBannerCount"),

]