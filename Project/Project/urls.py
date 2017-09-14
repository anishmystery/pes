"""helloapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib import admin
from PES.views import signin, login, addemp, viewtech, addtech, alltech, adtskills, revskill
from PES.views import allnontech, addmanager, home, techskills, alloctech, allocaddt, skillreview
from PES.views import viewnontech, addnontech, ntskills, allocmgr, allocnontech, alladdt, revaddskill
from PES.views import logout, detailsemp, allmgr, emphome, distech, disnon, revindex, deactivate, addtskillreview

urlpatterns = [
    #Login URLs
    url(r'^$', login),
    url(r'signin',signin),
    url(r'logout',logout),
    
    #Admin URLs
    url(r'home',home),
    url(r'detailsemp',detailsemp),
    url(r'addemp',addemp),
    url(r'viewtech',viewtech),
    url(r'viewnontech',viewnontech),
    url(r'alloctech',alloctech),
    url(r'allocnontech',allocnontech),
    url(r'allnontech',allnontech),
    url(r'addmanager',addmanager),
    url(r'addtech',addtech),
    url(r'techskills',techskills),
    url(r'addnontech',addnontech),
    url(r'ntskills',ntskills),
    url(r'alltech',alltech),
    url(r'allmgr',allmgr),
    url(r'allocmgr',allocmgr),
    url(r'deactivate=(?P<eid>\d+)',deactivate),

    #Employee URLs
    url(r'emp',emphome),
    url(r'distech',distech),
    url(r'disnon',disnon),
    url(r'adtskills',adtskills),
    url(r'alladdt',alladdt),
    url(r'allocaddt',allocaddt),
    url(r'revindex',revindex),
    url(r'revskill=(?P<eid>\d+)',revskill),
    url(r'skillreview=(?P<eid>\d+)',skillreview),
    url(r'revaddskill=(?P<eid>\d+)',revaddskill),
    url(r'addtreview=(?P<eid>\d+)',addtskillreview),
]
