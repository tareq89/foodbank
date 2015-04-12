
import time
import urllib2
from urllib2 import urlopen
import re
import datetime
import json
import re
from bs4 import BeautifulSoup


def Read(filepath):
	file = open(filepath, 'r')
	text = file.read()
	# print text
	return text

 
def Write(data,path):
	file = open(path, 'w').write(data)
		

def CollectMainLinks(url):
	# sourceCode = Read("prothom-alo.html")
	sourceCode = urllib2.urlopen(url).read()
	soup = BeautifulSoup(sourceCode, from_encoding="sourceCode")			
	div = soup.html.body	
	content = soup.select('#main-menu ul .menu_color_ .dynamic')
	links = []
	import re
	# print content
	# print content
	for x in content:
		# print x
		links = re.findall(r'href="(.*?)"', str(x))
		for y in links:
			print y
			links.append(y)
	return (json.dumps(links))

todaysLimit = None
page = 1
AllSubPagesLink = []
CurrentLyVisitingLink = None

def CollectSubPageLinks(url):

	shouldVisitNexPage = True
	global todaysLimit 
	global page
	global AllSubPagesLink
	global CurrentLyVisitingLink
	# print url
	sourceCode = Read("/home/tareq/Documents/Thesis_Scrapper/ProthomAloScrapper/bangladesh-article.html")
	# sourceCode = urllib2.urlopen(url).read()
	soup = BeautifulSoup(sourceCode)

	content = soup.findAll("div", attrs={"class":"oh mb10"})
	# content = soup.findAll("div", attrs={"class":"content_right"})

	for x in content:

		try:
			Imagelink = x.select('img')
			image = re.findall(r'<img .*?src="//(.*?)"', str(Imagelink))		
			Imagelink = "http://"+str(image[0])
			print Imagelink
		except Exception, e:
			print "No Image"


		title = x.select('a')
		title = re.findall(r'<a href=".*?">(.*?)</a>', str(title))
		try:
			title = title[0]
		except Exception, e:
			print title			
		

		link = x.select('a')
		link = re.findall(r'<a href="(.*?)"', str(link))
		try:
			link = url + link[0]
		except Exception, e:
			print link			
		

		additionalInfo = x.select('.additional_info')
		additionalInfoSource = re.findall(r'<span .*?>(.*?)</span>', str(additionalInfo)) 
		try:
			additionalInfoSource = additionalInfoSource[0]
		except Exception, e:
			print additionalInfoSource			

		additionalInfoTime = re.findall(r'<span>(.*?)</span>', str(additionalInfo)) 
		try:
			additionalInfoTime = additionalInfoTime[0]
		except Exception, e:
			print additionalInfoTime			

		subStory = x.select('.content')
		subStory = re.findall(r'<a href=".*?">(.*?)</a>', str(subStory))		
		for x in subStory:
			subStory = x
			break

		if todaysLimit == None:
			todaysLimit = str(additionalInfoTime[15:])
		print title
		print link
		print additionalInfoSource
		print additionalInfoTime
		print subStory
		
		print "\n\n\n"
		
		if (additionalInfoTime!=None) & (additionalInfoTime[15:] != todaysLimit):
			shouldVisitNexPage = False
			page = 1
			break
		else:
			AllSubPagesLink.append(title)
	# if shouldVisitNexPage:
	# 	page += 1
	# 	CollectSubPageLinks(CurrentLyVisitingLink+"?page="+str(page))

def Details(url):
	print url
	sourceCode = urllib2.urlopen(url).read()
	# sourceCode = Read("/home/tareq/Documents/Thesis_Scrapper/ProthomAloScrapper/details.html")
	soup = BeautifulSoup(sourceCode)
	content = soup.h1.text.encode('utf-8')
	print content
	content = soup.article
	# print content
	try:
		print content.img['src']
	except Exception, e:
		print "No Image"
	# print content
	articleLines =[]
	content = re.findall(r'<p.*?>(.*?)</p>', str(content))	
	for x in content:					
		x = re.sub(r'<img .*?/>', '', str(x))	
		x = re.sub(r'<br/>', '\n', str(x))	
		x = re.sub(r'<span>', '', str(x))	
		x = re.sub(r'</span>', '', str(x))
		x = re.sub(r'<strong>', '', str(x))
		x = re.sub(r'</strong>', '', str(x))	
		# print x+"\n\n"
		# print x
		articleLines.append(x)
	print json.dumps(articleLines)
	return None




def HeadLines(url):
	sourceCode = urllib2.urlopen(url).read()
	# sourceCode = Read("/home/tareq/Documents/Thesis_Scrapper/ProthomAloScrapper/details.html")
	soup = BeautifulSoup(sourceCode)
	content = soup.findAll("div", attrs={"class":"each_news mb20"})
	# print content
	for x in content:
		# print x
		print "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
		# link = x.a['href']
		# print link
		try:
			link = x.select('a')
			link = re.findall(r'<a href="(.*?)"', str(link))

			link = url + link[0]
			shortLink = re.findall(r'^(.*/d?)', str(link))
			# print "this is shortlink : " + str(shortLink)
			link = shortLink[0]

			print link
		except Exception, e:
			print "No Link"
		try:
			image = re.findall(r'<img .*?src="//(.*?)"', str(x))
			print image[0]
		except Exception, e:
			print "No Image"
		
		try:
			title = re.findall(r'<a.*?>(.*?)</a>', str(x.h2.a))
			print title[0]
		except Exception, e:
			print "no Heading"

		try:
			subStory = re.findall(r'<a class="content_right".*?>(.*?)</a>', str(x))
			print subStory[0]
		except Exception, e:
			print "No subStory"



def MainHeadings():
	url = "http://www.prothom-alo.com/"
	sourceCode = urllib2.urlopen(url).read()
	# sourceCode = Read("/home/tareq/Documents/Thesis_Scrapper/ProthomAloScrapper/details.html")
	soup = BeautifulSoup(sourceCode)
	MARQUEEContent = soup.marquee
	print MARQUEEContent
	for x in MARQUEEContent:
		print x
		try:
			
			link = re.findall(r'<a .*href="(.*?)"', str(x))

			link = url + link[0]
			shortLink = re.findall(r'^(.*/d?)', str(link))
			# print "this is shortlink : " + str(shortLink)
			url = shortLink[0]

			print url
		except Exception, e:
			# print "No Link"
			pass

		sourceCode = urllib2.urlopen(url).read()
		soup = BeautifulSoup(sourceCode)
		heading = soup.h1.text.encode('utf-8')
		print heading		
		content = soup.article		
		try:
			print content.img['src']
		except Exception, e:
			print "No Image"		

		# content = re.findall(r'<p.*?>(.*?)</p>', str(content))	
		# for x in content:					
		# 	x = re.sub(r'<img .*?/>', '', str(x))	
		# 	x = re.sub(r'<br/>', '\n', str(x))	
		# 	x = re.sub(r'<span>', '', str(x))	
		# 	x = re.sub(r'</span>', '', str(x))
		# 	x = re.sub(r'<strong>', '', str(x))
		# 	x = re.sub(r'</strong>', '', str(x))	
		# 	print x
		# 	# print x

		# # return None
		

# MainHeadings()

# HeadLines("http://www.prothom-alo.com/")

URL = ["http://www.prothom-alo.com/bangladesh/article/366082/",
"http://www.prothom-alo.com/bangladesh/article/366073/",
"http://www.prothom-alo.com/bangladesh/article/366079/",
"http://www.prothom-alo.com/bangladesh/article/366061/",
"http://www.prothom-alo.com/bangladesh/article/366070/",
"http://www.prothom-alo.com/bangladesh/article/366052/",
"http://www.prothom-alo.com/bangladesh/article/366058/",
"http://www.prothom-alo.com/bangladesh/article/366043/",
"http://www.prothom-alo.com/bangladesh/article/366046/",
"http://www.prothom-alo.com/bangladesh/article/366049/",
"http://www.prothom-alo.com/bangladesh/article/366034/",
"http://www.prothom-alo.com/bangladesh/article/366037/",
"http://www.prothom-alo.com/bangladesh/article/366025/",
"http://www.prothom-alo.com/bangladesh/article/366028/",
"http://www.prothom-alo.com/bangladesh/article/366031/",
"http://www.prothom-alo.com/bangladesh/article/366016/",
"http://www.prothom-alo.com/bangladesh/article/366022/",
"http://www.prothom-alo.com/bangladesh/article/366007/",
"http://www.prothom-alo.com/bangladesh/article/366010/",
"http://www.prothom-alo.com/bangladesh/article/365998/"]
i = 0
# for x in URL:
# 	i+=1
# 	print i
# 	Details(x)
url = "http://www.prothom-alo.com/bangladesh/article/472168/"
# url = "http://www.prothom-alo.com/bangladesh/article/472198/"
# url = "http://www.prothom-alo.com/bangladesh/article/409006/"
# Details(url)
# CollectMainLinks('http://www.prothom-alo.com/')

CurrentLyVisitingLink = "http://www.prothom-alo.com/bangladesh/article/"
# CollectSubPageLinks(CurrentLyVisitingLink)
# Write(json.dumps(AllSubPagesLink),"newsTitle.txt")
# print todaysLimit

Details("http://www.prothom-alo.com/bangladesh/article/466762/%E0%A6%9F%E0%A7%87%E0%A6%95%E0%A6%A8%E0%A6%BE%E0%A6%AB%E0%A7%87-%E0%A6%8F%E0%A6%95-%E0%A6%B2%E0%A6%BE%E0%A6%96-%E0%A6%87%E0%A6%AF%E0%A6%BC%E0%A6%BE%E0%A6%AC%E0%A6%BE-%E0%A6%89%E0%A6%A6%E0%A7%8D%E0%A6%A7%E0%A6%BE%E0%A6%B0")


# sourceCode = urllib2.urlopen("http://127.0.0.1:8000/rest/subpages").read()
# sourceCode = json.loads(sourceCode)
# for x in sourceCode:
# 	print x.encode('utf-8')
# print sourceCode.encode('utf-8')


# url = "http://127.0.0.1:8000/rest/details?url=http://www.prothom-alo.com/bangladesh/article/471541/"
# sourceCode = urllib2.urlopen(url).read()
# sourceCode = json.loads(sourceCode)
# for x in sourceCode:
# 	print x.encode('utf-8')