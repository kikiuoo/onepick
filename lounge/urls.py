from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),

    path("notice/viewer/<int:num>/", views.notice, name="notice"),
    path("notice/list/<int:page>/", views.notiList, name="notiList"),

    path("qanda/list/<int:page>/", views.qandaList, name="qandaList"),
    path("qanda/myList/<int:page>/", views.qandaMyList, name="qandaMyList"),
    path("qanda/write/", views.qandaWrite, name="qandaWrite"),
    path("qanda/writeCallBack/", views.qandaWriteCallBack, name="qandaWriteCallBack"),
    path("qanda/edit/<int:num>/", views.qandaEdit, name="qandaEdit"),
    path("qanda/editCallBack/", views.qandaEditCallBack, name="qandaEditCallBack"),
    path("qanda/delete/<int:num>/", views.qandaDelete, name="qandaDelete"),

    path("qanda/viewer/<int:num>/", views.qandaView, name="qandaView"),
    path("qanda/ajax/saveComment/", views.qaSaveComment, name="qaSaveComment"),
    path("qanda/ajax/reloadComment/", views.qaReloadComment, name="qaReloadComment"),
    path("qanda/ajax/deleteComment/", views.qaDeleteComment, name="qaDeleteComment"),

    path("magazine/list/<int:page>/", views.magaList, name="magaList"),
    path("magazine/viewer/<int:num>/", views.magaView, name="magaView"),
    path("magazine/write/", views.magaWrite, name="magaWrite"),
    path("magazine/writeCallBack/", views.magaWriteCallBack, name="magaWriteCallBack"),
    path("magazine/edit/<int:num>/", views.magaEdit, name="magaEdit"),
    path("magazine/editCallBack/", views.magaEditCallBack, name="magaEditCallBack"),
    path("magazine/delete/<int:num>/", views.magaDelete, name="magaDelete"),
    path("magazine/ajax/saveComment/", views.magaSaveComment, name="magaSaveComment"),
    path("magazine/ajax/reloadComment/", views.magaReloadComment, name="magaReloadComment"),
    path("magazine/ajax/deleteComment/", views.magaDeleteComment, name="magaDeleteComment"),

    path("bull/list/<int:page>/", views.bullList, name="magaList"),
    path("bull/viewer/<int:num>/", views.bullView, name="magaView"),
    path("bull/write/", views.bullWrite, name="magaWrite"),
    path("bull/writeCallBack/", views.bullWriteCallBack, name="magaWriteCallBack"),
    path("bull/edit/<int:num>/", views.bullEdit, name="bullEdit"),
    path("bull/editCallBack/", views.bullEditCallBack, name="bullEditCallBack"),
    path("bull/delete/<int:num>/", views.bullDelete, name="bullDelete"),
    path("bull/ajax/saveComment/", views.bullSaveComment, name="magaSaveComment"),
    path("bull/ajax/reloadComment/", views.bullReloadComment, name="magaReloadComment"),
    path("bull/ajax/deleteComment/", views.bullDeleteComment, name="magaDeleteComment"),
]