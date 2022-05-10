from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("ajax/updatePick/", views.updatePick, name="ajax-updatepick"),
]