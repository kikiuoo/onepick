from django.urls import path
from . import views

urlpatterns = [
    path('list/<cate_type>/<orderby>/', views.listView, name='listView'),
    path('profileDetail/<cate_type>/<int:num>/', views.viewer, name='listView'),
    path('ajax/<type>/<int:num>/', views.viewerDetail, name='listView'),
]