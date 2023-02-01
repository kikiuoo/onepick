"""myonepick URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    #path('', include('picktalk.urls')),
    path('', include('website.urls.urls')),
    path('profile/', include('website.urls.profile_urls')),
    path('audi/', include('website.urls.audition_urls')),
    path('lounge/', include('website.urls.lounge_urls')),
    path('users/', include('website.urls.user_urls')),
    path('ajax/', include('website.urls.ajax_urls')),
    path('search/', include('website.urls.search_urls')),
    path('common/', include('website.urls.common_urls')),
    path('login/', include('website.urls.login_urls')),

    path('onepickAdmin/', include('onepickAdmin.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
