# import facebook
import json, ast
from django.db import models

# from django.conf import settings
# settings.configure()

import django
from Insert.models import *

from django.core import serializers




def WriteFile(json):
	file = open("json2.txt", "w")
	file.write(json)
	file.close()

def ReadFile(filename):
	# file = open("foodbank.txt", "r")
	file = open(filename, "r")
	text = file.read()
	# return jsonDump(text)
	return text

def jsonDump(object):
	return json.dumps(object, separators=(',',':'))


def DjangoJson(object):
	data = serializers.serialize("json", [object,])
	return jsonDump(data)

def AssignPost(data):
	post 							=		Post()
	
	try:
		post.postId 					= 		data["id"]
	except Exception, e:
		print e.message
	
	
	try:
		post.userId 					= 		data["from"]["id"]
	except Exception, e:
		print e.message
	
	
	try:
		post.userName					=		unicode(data["from"]["name"])
	except Exception, e:
		print e.message
	
	
	try:
		post.message 					=		unicode(data["message"])
	except Exception, e:
		print e.message
	
	# print post.message
	
	try:
		post.pictureURL 				=		data["picture"]	
	except Exception, e:
		print e.message
	
	
	try:
		post.postURL					=		data["link"]
	except Exception, e:
		print e.message
	
	
	try:
		post.object_id 					=		data["object_id"]
	except Exception, e:
		print e.message
	
	
	try:
		post.created_time				=		data["created_time"]
	except Exception, e:
		print e.message
	
	
	try:
		post.updated_time				=		data["updated_time"]
	except Exception, e:
		print e.message
	

	try:
		post.commentAfter			=		data["comments"]["paging"]["cursors"]["after"]
	except Exception, e:
		print e.message		
	
	try:
		post.commentBefore			=		data["comments"]["paging"]["cursors"]["before"]
	except Exception, e:
		print e.message		
	
	try:
		post.likeAfter				=		data["likes"]["paging"]["cursors"]["after"]
	except Exception, e:
		print e.message		
	
	try:
		post.likeBefore			=		data["likes"]["paging"]["cursors"]["before"]
	except Exception, e:
		print e.message		
	
	# print DjangoJson(post)
	post.save()
	print post.id

	

	try:
		for x in data["likes"]["data"]:
			like 				= 		Likes()
			
			try:
				like.userId			=		x["id"]
			except Exception, e:
				print e.message
			
			
			try:
				like.userName		=		unicode(x["name"])
			except Exception, e:
				print e.message
			
			
			try:
				like.Post			=		post
			except Exception, e:
				print e.message
			
	
			# print DjangoJson(like)
			like.save()

	except Exception, e:
		print "print exception : " + e.message


	try:
		for x in data["comments"]["data"]:
			comment  			=		Comments()
			try:
				comment.commentId			=		x["id"]	
			except Exception, e:
				print e.message


			try:
				comment.userId				=		x["from"]["id"]
			except Exception, e:
				print e.message


			try:
				comment.userName			=		unicode(x["from"]["name"])
			except Exception, e:
				print e.message


			try:
				comment.message				=		unicode(x["message"])
			except Exception, e:
				print e.message


			try:
				comment.created_time		=		x["created_time"]
			except Exception, e:
				print e.message


			try:
				comment.Post				=		post
			except Exception, e:
				print e.message


			comment.save()

	except Exception, e:
		print "comment exception : " + e.message

	try:
		sentiment					=		Sentiment()
		try:
			sentiment.pos 			=		data["sentiment"]["pos"]
		except Exception, e:
			print e.message
		try:
			sentiment.neg 			=		data["sentiment"]["neg"]
		except Exception, e:
			print e.message
		try:
			sentiment.sentiment 	=		data["sentiment"]["sentiment"]
		except Exception, e:
			print e.message
		try:
			sentiment.Post 			=		post
		except Exception, e:
			print e.message
		print sentiment
		 
		sentiment.save()
	except Exception, e:
		print e.message

	try:		
		application					=		Application()		
		try:
			application.name 			=		data["application"]["name"]				
		except Exception, e:
			print e.message


		try:
			application.namespace		=		data["application"]["namespace"]
		except Exception, e:
			print e.message


		try:
			application.app_id			=		data["application"]["id"]
		except Exception, e:
			print e.message


		try:
			application.Post			=		post
		except Exception, e:
			print e.message

		application.save()	

	except Exception, e:
		print "Apllication exception " + e.message




	try:
		for x in data["message_tags"]:
			# print data["message_tags"][x][0]["name"]
			message_tags				=		Message_Tags()
			
			try:
				message_tags.tagId			=		data["message_tags"][x][0]["id"]
			except Exception, e:
				print e.message

			
			try:
				message_tags.tagName		=		unicode(data["message_tags"][x][0]["name"])
			except Exception, e:
				print e.message

			
			try:
				message_tags.taggedIdType	=		data["message_tags"][x][0]["type"]
			except Exception, e:
				print e.message

			
			try:
				message_tags.Post 			=		post
			except Exception, e:
				print e.message


			message_tags.save()
	except Exception, e:
		print "Apllication exception " + e.message



	try:

		place 							=		Place()
		

		try:
			place.PlaceId					=		data["place"]["id"]
		except Exception, e:
			print e.message
		

		try:
			place.Name						=		unicode(data["place"]["name"])
		except Exception, e:
			print e.message
		

		try:
			place.City						=		data["place"]["location"]["city"]
		except Exception, e:
			print e.message
		

		try:
			place.Country					=		data["place"]["location"]["country"]
		except Exception, e:
			print e.message
		

		try:
			place.Street					=		data["place"]["location"]["street"]
		except Exception, e:
			print e.message
		

		try:
			place.Longitude					=		data["place"]["location"]["longitude"]
		except Exception, e:
			print e.message
		

		try:
			place.Latitude					=		data["place"]["location"]["latitude"]
		except Exception, e:
			print e.message
		

		try:
			place.Post						=		post
		except Exception, e:
			print e.message


		place.save()
	except Exception, e:
		print "Apllication exception " + e.message