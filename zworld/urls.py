"""zworld URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin

from social_zone import views as sovs

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', sovs.social),
    url(r'^user$', sovs.sign),
    url(r'^edu$', sovs.edu),
    url(r'^work$', sovs.work),
    url(r'^diary', sovs.diary),
    url(r'^friend$', sovs.friend),
    url(r'^message', sovs.message),
    url(r'^personalinfo', sovs.personal),
    url(r'^userupdate', sovs.user_update),
    url(r'^eduinsert', sovs.edu_insert),
    url(r'^workinsert', sovs.work_insert),
    url(r'^search_friend', sovs.search_friend),
    url(r'^add_friend$', sovs.add_friend),
    url(r'^add_group', sovs.add_group),
    url(r'^friend_info', sovs.friend_info),
    url(r'^add_friend_to_group', sovs.add_friend_to_group),
    url(r'^delete_friend', sovs.delete_friend),


]
