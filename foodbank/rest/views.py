from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader, RequestContext
from django.template import loader, Context
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django import forms
import json
from django.http import HttpResponse
from django.core import serializers
import urllib2
from urllib2 import urlopen
import json
from bs4 import BeautifulSoup
import re
 

class News(object):
	def __init__(self):
		self.subStory = None
		self.additionalInfoTime = None
		self.additionalInfoSource = None
		self.link = None
		self.title = None
		self.imageLink = None

		class Meta:
			app_label = 'rest'

class DetailsNews(object):
	def __init__(self):
		self.Story = None
		self.Imagelink = None
		self.title = None

		class Meta:
			app_label = 'rest'


class HeadLine(object):
	"""docstring for HeadLine"""
	def __init__(self):
		self.Title = None
		self.SubStory = None
		self.Imagelink = None
		self.Link = None

		
def FirstPage(request):
	url = "http://www.prothom-alo.com/"
	print url
	# sourceCode = "halum"
	sourceCode = urllib2.urlopen(url).read()
	soup = BeautifulSoup(sourceCode, from_encoding="sourceCode")			
	div = soup.html.body	
	content = soup.select('#main-menu ul .menu_color_ .dynamic')
	links = re.findall(r'href="(.*?)"', str(content))
	return HttpResponse(json.dumps(links))	
 

 
# CurrentLyVisitingLink = "http://www.prothom-alo.com/bangladesh/article/"

 
def CollectSubPageLinks(request):

	if request.method == 'GET':
		print "true"
		CurrentLyVisitingLink = request.GET.get('url', '')
		print CurrentLyVisitingLink
	AllSubPagesLink = CollectSubPageLinksMethod(CurrentLyVisitingLink)

	NewsListJson = []
	NewsListJson += "["
	i = 0
	for x in AllSubPagesLink:
		x = json.dumps(vars(x))
		NewsListJson.append(x)
		i += 1
		if len(AllSubPagesLink) > i:
			NewsListJson+= ","
	NewsListJson += "]"
	return HttpResponse(NewsListJson)





def CollectSubPageLinksMethod(url):	
	AllSubPagesLink = []
	sourceCode = urllib2.urlopen(url).read()
	soup = BeautifulSoup(sourceCode)

	content = soup.findAll("div", attrs={"class":"oh mb10"})


	imageSoup = soup.findAll("img")
	print "Image : " + str(imageSoup)
	# print "\n\n\n\n\n\n\n\n\n\n\n\n****************************************************************"
	for x in content:

		news = News()


		try:
			Imagelink = x.select('img')
			image = re.findall(r'<img .*?src="//(.*?)"', str(Imagelink))		
			news.imageLink = "http://"+str(image[0])
			print Imagelink
		except Exception, e:
			print "No Image"



		title = x.select('a')
		title = re.findall(r'<a href=".*?">(.*?)</a>', str(title))
		try:
			title = title[0]
			news.title = title
		except Exception, e:
			print "Exception : " + str(e) + "\n"			
		

 			# 	link = x.select('a')
			# link = re.findall(r'<a href="(.*?)"', str(link))

			# link = url + link[0]
			# shortLink = re.findall(r'^(.*/d?)', str(link))
			# # print "this is shortlink : " + str(shortLink)
			# link = shortLink[0]
			# headline.Link = link


		link = x.select('a')
		link = re.findall(r'<a href="(.*?)"', str(link))
		try:
			link = url + link[0]
			shortLink = re.findall(r'^(.*/d?)', str(link))
			# print "this is shortlink : " + str(shortLink)
			news.link = shortLink[0]
		except Exception, e:
			print link			
		

		additionalInfo = x.select('.additional_info')
		additionalInfoSource = re.findall(r'<span .*?>(.*?)</span>', str(additionalInfo)) 
		try:
			additionalInfoSource = additionalInfoSource[0]
			news.additionalInfoSource = additionalInfoSource
		except Exception, e:
			print "Exception : " + str(e) + "\n"			

		additionalInfoTime = re.findall(r'<span>(.*?)</span>', str(additionalInfo)) 
		try:
			additionalInfoTime = additionalInfoTime[0]
			news.additionalInfoTime = additionalInfoTime
		except Exception, e:
			print "Exception : " + str(e) + "\n"			

		subStory = x.select('.content')
		subStory = re.findall(r'<a href=".*?">(.*?)</a>', str(subStory))		
		for x in subStory:
			subStory = x
			news.subStory = subStory
			break
		# print news.title
		# if todaysLimit == None:
		# 	todaysLimit = str(additionalInfoTime[15:])
		# print title
		# print link
		# print additionalInfoSource
		# print additionalInfoTime
		# print subStory
		# print "\n\n\n"
		AllSubPagesLink.append(news)
	return AllSubPagesLink





def Details(request):
	details = DetailsNews()
	if request.method == 'GET':
		print "true"
		CurrentLyVisitingLink = request.GET.get('url', '')
		print CurrentLyVisitingLink
	sourceCode = urllib2.urlopen(CurrentLyVisitingLink).read()
	soup = BeautifulSoup(sourceCode)	
	details.title = soup.h1.text.encode('utf-8')
	content = soup.article
	# print content
	try:
		details.Imagelink = content.img['src']
	except Exception, e:
		print "No Image"
	# print content
	print "\n\n\n\n"
	articleLines = []
	content = re.findall(r'<p.*?>(.*?)</p>', str(content))	
	for x in content:					
		x = re.sub(r'<img .*?/>', '', str(x))	
		x = re.sub(r'<br/>', '\n', str(x))	
		x = re.sub(r'<span>', '', str(x))	
		x = re.sub(r'</span>', '', str(x))
		x = re.sub(r'<strong>', '', str(x))
		x = re.sub(r'</strong>', '', str(x))
		x = re.sub(r'<em>', '', str(x))
		x = re.sub(r'</em>', '', str(x))	
		articleLines.append(x)
	details.Story = articleLines
	return HttpResponse(json.dumps(vars(details)))




def HeadLines(request):
	headlines = []	
	url = "http://www.prothom-alo.com/"
	sourceCode = urllib2.urlopen(url).read()
	soup = BeautifulSoup(sourceCode)
	content = soup.findAll("div", attrs={"class":"each_news mb20"})
	# print content
	for x in content:
		headline = HeadLine()
		# print x
		# print "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
		try:
			link = x.select('a')
			link = re.findall(r'<a href="(.*?)"', str(link))

			link = url + link[0]
			shortLink = re.findall(r'^(.*/d?)', str(link))
			# print "this is shortlink : " + str(shortLink)
			link = shortLink[0]
			headline.Link = link
			# print link
		except Exception, e:
			print "No Link"

		try:
			image = re.findall(r'<img .*?src="//(.*?)"', str(x))
			# print image[0]
			headline.Imagelink = "http://"+str(image[0])
			print headline.Imagelink
		except Exception, e:
			print "No Image"
		
		try:
			title = re.findall(r'<a.*?>(.*?)</a>', str(x.h2.a))
			# print title[0]
			headline.Title = title[0]

		except Exception, e:
			print "no Heading"

		try:
			subStory = re.findall(r'<a class="content_right".*?>(.*?)</a>', str(x))
			# print subStory[0]
			headline.SubStory = subStory[0]
		except Exception, e:
			print "No subStory"

		headlines.append(headline)

	NewsListJson = []
	NewsListJson += "["
	i = 0
	for x in headlines:
		x = json.dumps(vars(x))
		NewsListJson.append(x)
		i += 1
		if len(headlines) > i:
			NewsListJson+= ","
	NewsListJson += "]"
	return HttpResponse(NewsListJson)
	

def HelloFromViews(request):
	return HttpResponse("Hi")