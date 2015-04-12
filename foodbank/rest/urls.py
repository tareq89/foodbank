from django.conf.urls import patterns, url
from rest import views


urlpatterns = patterns('',
	url(r'^firstpage', views.FirstPage, name='FirstPage'),
	url(r'^subpages', views.CollectSubPageLinks, name='CollectSubPageLinks'),
	url(r'^details', views.Details, name='Details'),
	url(r'^headlines', views.HeadLines, name='HeadLines'),
	url(r'^hi', views.HelloFromViews, name='HelloFromViews'),
)