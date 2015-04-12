from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader, RequestContext
from Insert.models import *
from Insert.functions.populateDB import *
from django.template import loader, Context
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django import forms
import json
from django.http import HttpResponse
from django.core import serializers
from decimal import Decimal
import math
# from Insert.functions.sentimentAnalyseBasedOnWordVal import *
from Insert.functions.distanceCalculate import DistanceClaculate
class UNIQ_PLACES_CLASS(object):
	"""docstring for UNIQ_PLACES_CLASS"""
	def __init__(self):		
		self.PlaceId = None
		self.Name = None
		self.City = None
		self.Country = None
		self.Street = None
		self.Longitude = None
		self.Latitude = None
		self.Post_id = None
		self.index = None
		self.distance = None
		self.rating = None
		self.messageList = None


class RatingMarker(object):
	"""docstring for RatingMarker"""
	def __init__(self):
		self.arg = "a"
		



# Create your views here.
def firstpage(request):
	return render_to_response('index/index.html')

def firstpageRequest(request):
	import json
	print "this is from firstpageRequest"

	query = ""
####################################################################################
#
#		REQUEST PARAMTER RETRIEVING
#
####################################################################################
	if request.method == 'GET':
		print "true"
		# for hasib, use as many fields in the input form and write respective codes
		# like
		#  query = request.GET.get('**YOUR DEFINED PARAMETER**', '')
		#  and than print it or append with HttpResponse(query)
		query = request.GET.get('query', '')
		cbox = json.loads(request.GET.get('cbox', '')) # u know what it is :/
		ratingQuery = request.GET.get('rating', '') # don't forget to make them int
		distance = request.GET.get('distance', '') # float would be better I guess :s
		location  = json.loads(request.GET.get('location', '')) # lat, lon are float :/
		print distance
		print location["lat"]

		

####################################################################################
#
#		PLACES DETAILS ACCORDING TO QUERY
#
####################################################################################
	SINGLE_PLACE_DETAILS_QUERY = """SELECT *
					FROM "public"."Insert_place" 
					WHERE "public"."Insert_place"."PlaceId" = %s """
	
	SINGLE_PLACE_DETAILS = Post.objects.raw(SINGLE_PLACE_DETAILS_QUERY, ["1506397029572029"])


####################################################################################
#
#		UNIQ PLACES LIST ACCORDING TO QUERY
#
####################################################################################
	UNIQ_PLACES_LIST_QUERY = """SELECT 
										"public"."Insert_place"."id",
									  	"public"."Insert_place"."Name"
								FROM
											"public"."Insert_post" 
								INNER JOIN 	"public"."Insert_place"
								ON 
											"public"."Insert_post"."id" 
										= 	"public"."Insert_place"."Post_id"
								WHERE "public"."Insert_post"."message" LIKE %s
								ORDER BY "public"."Insert_place"."Name"
								 """
	UNIQ_PLACES_LIST = Place.objects.raw(UNIQ_PLACES_LIST_QUERY, ['%'+query+'%'])

	UNIQ_PLACES_NAME_list = []
	UNIQ_PLACES = []
	i = 0
	for x in UNIQ_PLACES_LIST:
		if x.Name not in UNIQ_PLACES_NAME_list:
			UNIQ_PLACES_NAME_list.append(x.Name)

			y = UNIQ_PLACES_CLASS()
			y.PlaceId = x.PlaceId
			y.Name = x.Name
			y.City = x.City
			y.Country = x.Country
			y.Street = x.Street
			y.Longitude = x.Longitude
			y.Latitude = x.Latitude
			y.Post_id = x.Post_id

			y.index = i
			i += 1


			if location["lat"] != None:				 
				y.distance = DistanceClaculate(location['lat'],location['lon'],x.Latitude, x.Longitude)

			SENTIMENT_QUERY = """ SELECT "public"."Insert_sentiment"."id", "public"."Insert_sentiment"."pos",
				 "public"."Insert_sentiment"."neg" 

				FROM "public"."Insert_place",
				"public"."Insert_sentiment"

				WHERE   "public"."Insert_place"."Post_id" = "public"."Insert_sentiment"."Post_id"
				 AND "public"."Insert_place"."PlaceId" = %s  """

			sentiment = Sentiment.objects.raw(SENTIMENT_QUERY, [x.PlaceId])
			allPos = 0.00
			allNeg = 0.00
			count = 0.0
			for s in sentiment:
				count+=1
				if s.pos==0.0 and s.neg==0.0:
					allPos+=0.5
					allNeg+=0.5
				allPos += float(s.pos)
				allNeg += float(s.neg)

			rating = int(math.ceil((10.00*allPos/count)/2.00))
			if rating == 0:
				rating = 1
			y.rating = []
			for z in xrange(1,rating):
				y.rating.append(RatingMarker())
			# print "sentiment : "+ str(y.rating)






			####################################################################################
			#
			#		PLACES WITH POSTS ACCORDING TO QUERY
			#
			####################################################################################
			ONE_PLACE_ALL_POSTS_QUERY = """ SELECT "public"."Insert_post"."id", "public"."Insert_post"."message"
							FROM "public"."Insert_post" INNER JOIN "public"."Insert_place"
							ON "public"."Insert_post"."id" = "public"."Insert_place"."Post_id"
							WHERE "public"."Insert_post"."message" LIKE %s
							AND "public"."Insert_place"."PlaceId" = %s				
							LIMIT 200"""

			ONE_PLACE_ALL_POSTS = Post.objects.raw(ONE_PLACE_ALL_POSTS_QUERY, ['%'+query+'%', x.PlaceId])
			messageList = []
			for x in ONE_PLACE_ALL_POSTS:
				messageList.append(x.message)

			y.messageList = messageList			
			if float(y.distance) <= float(distance):
				if len(y.rating) >= int(ratingQuery):
					print "y.rating :" + str(len(y.rating)) +"    ratingQuery : " + str(ratingQuery)
					UNIQ_PLACES.append(y)
			


# PlaceId 	Name 	City 	Country 	Street 	Longitude 	Latitude 	Post_id
####################################################################################
#
#		
#
####################################################################################


	print "length ", len(UNIQ_PLACES)
	context = RequestContext(request, {
				'query' : query,				
				'uniq_place_list': UNIQ_PLACES,
				'place_details': SINGLE_PLACE_DETAILS[0]
			})
 
 	# return render_to_response('resultpage/index.html', context)
 	return render_to_response('result/index.html', context)


def PlacePostRetrun(request):
	import json
	if request.method == 'GET':
		print "true"
		query = request.GET.get('query', '')
		placeid = request.GET.get('placeid', '')
####################################################################################
#
#		PLACES WITH POSTS ACCORDING TO QUERY
#
####################################################################################
	ONE_PLACE_ALL_POSTS_QUERY = """ SELECT "public"."Insert_post"."id", "public"."Insert_post"."message"
					FROM "public"."Insert_post" INNER JOIN "public"."Insert_place"
					ON "public"."Insert_post"."id" = "public"."Insert_place"."Post_id"
					WHERE "public"."Insert_post"."message" LIKE %s
					AND "public"."Insert_place"."PlaceId" = %s				
					LIMIT 200"""
	# 1506397029572029
	ONE_PLACE_ALL_POSTS = Post.objects.raw(ONE_PLACE_ALL_POSTS_QUERY, ['%'+query+'%', placeid])
	messageList = []
	for x in ONE_PLACE_ALL_POSTS:
		messageList.append(x.message)

	return HttpResponse(json.dumps(messageList));

	
def insert(request):
	import json
	import os
	# latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
	# template = loader.get_template('Views/index.html')
	# context = Context({
	# 	'latest_poll_list': latest_poll_list,
	# 	})
	
	

	filename = os.path.realpath("Insert/json2WithSentiment.txt")
	file = open(filename, "r")
	text = file.read()

	Data = json.loads(text)

	# data = Data[300]

	# AssignPost(data)
	# AssignPost(Data[2]) 
	# print data

	# for data in Data:		
	# 	AssignPost(data) 
	# 	print "post "


	# print DjangoJson(post)
	# post.save()
	return HttpResponse("Hello django !\n" + str(data))

def posts(request):
	posts = Post.objects.all().order_by('-created_time')
	context = RequestContext(request, {
			'posts': posts
		})
 	return render_to_response('posts/index.html', context)

class SearchPost(forms.Form):
	a = forms.CharField(label='Search topic' ,max_length=100)
		

@csrf_exempt
def query(request):	
	val = ""
	if request.method == 'POST':
		print "true"
		form = SearchPost(request.POST)
		val = request.POST.get('name', '')
		print val		
				
		topic = '%'+val+'%'
		posts = Post.objects.raw('SELECT * FROM "public"."Insert_post" WHERE "message" LIKE %s', [topic])
		context = RequestContext(request, {
				'posts': posts,
				'query': val
			})
	 	return render_to_response('query/index.html', context)
	else:		
		context = RequestContext(request, {
				'query': val
			})
		print "This is the val : " + val
	 	return render_to_response('query/index.html', context)
 	# return render(request, 'query/index.html', {'query': val})


from django.db import connection
def json(request):
	cursor = connection.cursor()	
	cursor.execute('''SELECT 	 
								"public"."Insert_place"."Name",
								"public"."Insert_place"."Latitude",
								"public"."Insert_place"."Longitude" 			
										

								FROM 	"public"."Insert_post" INNER JOIN "public"."Insert_place" 
								ON "public"."Insert_post"."id" = "public"."Insert_place"."Post_id"
								LIMIT 10 ''')
	data = cursor.fetchall()
	# print data
	data = jsonDump(data)
	# data = serializers.serialize("json", data)
	# data = '''[
 #      ["Cox's Bazar", -33.890542, 151.274856, 4],
 #      ["Potenga", -33.923036, 151.259052, 5],
 #      ["Inani Beach", -34.028249, 151.157507, 3],
 #      ["Teknuf", -33.80010128657071, 151.28747820854187, 2],
 #      ["Halishohor Beach", -33.950198, 151.259302, 1]
 #    ]''';
 	# data = '{"name": "tareq"}'

	return HttpResponse(data, content_type='application/json')

def ajax(request):
	return render_to_response('ajax/index.html')

def place_post(request):
	print "this is from place_post"
	val = ""
	if request.method == 'GET':
		print "true"
		val = request.GET.get('name', '')
		print val	
	cursor = connection.cursor()	
	cursor.execute('''SELECT 	 
								"public"."Insert_post"."message"													
								FROM 	"public"."Insert_post" INNER JOIN "public"."Insert_place" 
								ON "public"."Insert_post"."id" = "public"."Insert_place"."Post_id"
								WHERE "public"."Insert_place"."Name" = %s''', [val])
	data = cursor.fetchall()
	# print data
	data = jsonDump(data)
	return HttpResponse(data)

 