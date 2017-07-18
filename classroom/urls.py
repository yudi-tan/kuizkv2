from django.conf.urls import url, handler404, include
from django.contrib import admin
from . import views

app_name = 'classroom' 

urlpatterns = [
	 # url(r'^(?P<pk>[0-9]+)/$', views.index.as_view(), name='index'),
	 url(r'^(?P<pk>[0-9]+)/$', views.detail, name = 'detail'),
	 url(r'^(?P<pk>[0-9]+)/createassignment/$', views.createassignment, name='createassignment'),
	 url(r'^(?P<pk>[0-9]+)/createannouncement/$', views.createannouncement, name='createannouncement'),
	 url(r'^(?P<pk>[0-9]+)/forum', include('forum.urls', namespace='forum')),
	 url(r'(?P<pk>[0-9]+)/classmembers/$', views.classmembers, name='classmembers')


 
]
