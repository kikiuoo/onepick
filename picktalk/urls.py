from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("ajax/updatePick/", views.updatePick, name="ajax-updatepick"),

    path("advertise/", views.advertise, name="advertisse"),
    path("advertise/callBack/", views.advertise_callBack, name="advertise-callback"),

    path("search/<cateType>/<search>/<int:page>/", views.searchList, name="searchList"),

]