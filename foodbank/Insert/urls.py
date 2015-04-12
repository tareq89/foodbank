from django.conf.urls import patterns, url

from Insert import views


urlpatterns = patterns('',
	url(r'^firstpageRequest', views.firstpageRequest, name='firstpageRequest'),
	url(r'^$', views.firstpage, name='firstpage'),
	url(r'^insert', views.insert, name='index'),
	url(r'^posts', views.posts, name='posts'),	
	url(r'^query', views.query, name='query'),
	url(r'^json', views.json, name='json'),	
	url(r'^ajax', views.ajax, name='ajax'),	
	url(r'^place_post', views.PlacePostRetrun, name='place_post'),
)
