"""constructure URL Configuration

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
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from main import views

urlpatterns = [
	url(r'^$', views.test),                                                                                # testing purposes
	url(r'^index/$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^question0/$', TemplateView.as_view(template_name='question0.html'), name='question0'),
    url(r'^question1/$', TemplateView.as_view(template_name='question1.html'), name='question1'),
    url(r'^question2/$', TemplateView.as_view(template_name='question2.html'), name='question2'),
    url(r'^question3/$', TemplateView.as_view(template_name='question3.html'), name='question3'),
    url(r'^result/$', TemplateView.as_view(template_name='result.html'), name='result'),  
    url(r'^user/', include('main.urls')),
    url(r'^admin/', admin.site.urls),
]