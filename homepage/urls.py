from django.conf.urls import url
from . import views
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^loggedin/$', views.loggedin, name='loggedin'),
	url(r'^createclassroom/$', views.createclassroom, name='createclassroom'),
	url(r'^joinclassroom/$', views.joinclassroom, name='joinclassroom'),
]

