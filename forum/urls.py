from django.conf.urls import url, handler404, include
from django.contrib import admin
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'forum' 

urlpatterns = [
	 # url(r'^(?P<pk>[0-9]+)/$', views.index.as_view(), name='index'),
	 url(r'^(?P<pk2>[0-9]+)/$', views.index, name='index'),
	 url(r'^(?P<pk2>[0-9]+)/(?P<pk3>[0-9]+)/$', views.detail, name="detail"),
	 url(r'^(?P<pk2>[0-9]+)/createpost/$', views.createforumpost, name='createforumpost'),
	 url(r'^(?P<pk2>[0-9]+)/(?P<pk3>[0-9]+)/createcomment/$', views.createcomment, name="createcomment"),
	 url(r'^(?P<pk2>[0-9]+)/forumpostapi/$', views.ForumpostList.as_view(), name="forumpostapi"),
	 url(r'^/commentapi/$', views.CommentList.as_view(), name="commentapi"),
	 url(r'^/forumapi/$', views.ForumList.as_view(), name="forumapi")

]

urlpatterns = format_suffix_patterns(urlpatterns)