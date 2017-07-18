from django.conf.urls import url, include
from . import views
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^register/$', views.register.as_view(), name='register'),
	url(r'^updateprofile/$', views.updateprofile, name='updateprofile'),
	url(r'^profile/(?P<pk>\d+)/$', views.profile, name='profile'),
]

