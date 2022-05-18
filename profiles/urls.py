from django.urls import path
from . import views

urlpatterns = [
    path('list/<cate_type>/<orderby>/', views.listView, name='listView'),
    path('profileDetail/<cate_type>/<int:num>/', views.viewer, name='listView'),
    path('ajax/<type>/<int:num>/', views.viewerDetail, name='listView'),

    path('write/', views.pofile_write, name="profile-write"),
    path('write/callback/', views.pofile_write_callback, name="profile-writeCallback"),

    path('ajax/getSubCate/', views.audiAjaxGetCate, name="profile-getCate"),
    path('ajax/getSubCate_etc/', views.audiAjaxGetCateEtc, name="profile-getCateEtc"),
]