from django.urls import path
from website.views import views

urlpatterns = [
    #path('', views.index, name='main'),
    path('', views.downstime, name='downstime'),
    path('index/', views.index, name='main'),

    path("advertise/", views.advertise, name="advertisse"),
    path("advertise/callBack/", views.advertise_callBack, name="advertise-callback"),

    path("proList/<type>/<int:page>/<num>/<filter>/", views.proList, name="proList"),
    path("proList2/<type>/<int:page>/<num>/<filter>/", views.proList2, name="proList"),
    path("applyList/<num>/", views.applyList, name="applyList"),

    path(".well-known/pki-validation/gsdv.txt", views.gsdv, name="gsdv"),

]