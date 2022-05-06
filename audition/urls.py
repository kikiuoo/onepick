from django.urls import path
from . import views

urlpatterns = [
    path('main/<cate_type>/', views.audi_index, name='audiIndex'),  # path( url , view def 명, 이름 )
    path('audiDetail/<cate_type>/<int:num>/', views.audi_detail, name='audiDetail'),
    path('write/', views.audi_write, name='audi-write'),
    path('ajax/getSubCate/', views.audiAjaxGetCate, name="audi-getCate"),
]