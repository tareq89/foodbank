from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.http import HttpResponse
admin.autodiscover()

def hi(response):
	return HttpResponse("HI")

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'MyDjangO.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^foodbank/', include('Insert.urls')),
	url(r'^rest/', include('rest.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^hi/', hi),
)
