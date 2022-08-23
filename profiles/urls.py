from django.urls import path
from . import views

urlpatterns = [
    path('list/<cate_type>/<int:page>/', views.listView, name='listView'),
    path('profileDetail/<cate_type>/<int:num>/', views.viewer, name='listView'),
    path('profileDetail_all/<cate_type>/<int:num>/', views.viewer_all, name='listView'),

    path('write/', views.pofile_write, name="profile-write"),
    path('write/callback/', views.pofile_write_callback, name="profile-writeCallback"),

    path('edit/<int:num>/', views.pofile_edit, name="profile-edit"),
    path('edit/callback/', views.pofile_edit_callback, name="profile-editCallback"),

    path('delete/<int:num>/', views.pofile_delete, name="profile-delete"),

    path('ajax/getSubCate/', views.audiAjaxGetCate, name="profile-getCate"),
    path('ajax/getSubCate_etc/', views.audiAjaxGetCateEtc, name="profile-getCateEtc"),
    #path('ajax/getProfile/', views.getProfile, name="profile-getProfile"),
    path('ajax/saveComment/', views.saveComment, name="profile-saveComment"),
    path('ajax/reloadComment/', views.reloadComment, name="profile-reloadComment"),
    path('ajax/deleteComment/', views.deleteComment, name="profile-deleteComment"),
    path('ajax/profileSuggest/', views.profileSuggest, name="profile-profileSuggest"),

    path('print/<type>/<int:num>/', views.printProfile, name="profile-print"),
]