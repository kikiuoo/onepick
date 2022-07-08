from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("ajax/updatePick/", views.updatePick, name="ajax-updatepick"),

    path("advertise/", views.advertise, name="advertisse"),
    path("advertise/callBack/", views.advertise_callBack, name="advertise-callback"),

    path("search/<cateType>/<search>/<int:page>/", views.searchList, name="searchList"),
    path("search/ajaxProfile/", views.getSearchProfile, name="getSearchProfile"),

    path("notice/viewer/<int:num>/", views.notice, name="notice"),
    path("notice/list/<int:page>/", views.notiList, name="notiList"),

    path("proList/<type>/<int:page>/<num>/", views.proList, name="proList"),

    path("qanda/list/<int:page>/", views.qandaList, name="qandaList"),

    path("qanda/write/", views.qandaWrite, name="qandaWrite"),
    path("qanda/writeCallBack/", views.qandaWriteCallBack, name="qandaWriteCallBack"),
    path("qanda/viewer/<int:num>/", views.qandaView, name="qandaView"),

    path("qanda/ajax/saveComment/", views.qaSaveComment, name="qaSaveComment"),
    path("qanda/ajax/reloadComment/", views.qaReloadComment, name="qaReloadComment"),
    path("qanda/ajax/deleteComment/", views.qaDeleteComment, name="qaDeleteComment"),

]