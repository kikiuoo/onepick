from django.urls import path
from . import views

urlpatterns = [
    path('regCompany/', views.regCompany, name='reg-company'),
    path('regCompany/callback/', views.regCompanyCallBack, name='reg-company-callback'),
]