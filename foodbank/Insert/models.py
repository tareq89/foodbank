from django.db import models



class Post(models.Model):
	postId 			= 		models.CharField(max_length = 50, null=True)
	userId 			= 		models.CharField(max_length = 20, null=True)
	userName		= 		models.CharField(max_length = 100, null=True)
	message 		= 		models.CharField(max_length = 10000, null=True)
	pictureURL 		= 		models.CharField(max_length = 1000, null=True)
	postURL			= 		models.CharField(max_length = 1000, null=True)
	object_id 		= 		models.CharField(max_length = 20, null=True)
	created_time	= 		models.CharField(max_length=100, null=True)
	updated_time	= 		models.CharField(max_length=100, null=True)
	commentAfter	= 		models.CharField(max_length = 200, null=True)
	commentBefore	= 		models.CharField(max_length = 200, null=True)
	likeAfter		= 		models.CharField(max_length = 200, null=True)
	likeBefore		= 		models.CharField(max_length = 200, null=True)

    
	class Meta:
		app_label = 'Insert'

	def __unicode__(self):
		return u'%s %s' % (self.message, self.userName)


class Sentiment(models.Model):
	pos 			=		models.DecimalField(null=True, max_digits=19, decimal_places=10)
	neg				=		models.DecimalField(null=True, max_digits=19, decimal_places=10)
	sentiment		=		models.CharField(max_length=10, null=True)
	Post 			=		models.ForeignKey(Post)
	class Meta:
		app_label = 'Insert'



class Application(models.Model):
	name 			= 		models.CharField(max_length = 40, null=True)
	namespace		= 		models.CharField(max_length = 40, null=True)
	app_id			= 		models.CharField(max_length = 40, null=True)
	Post			=		models.ForeignKey(Post)
	class Meta:
		app_label = 'Insert'

class Likes(models.Model):
	userId			= 		models.CharField(max_length = 20, null=True)
	userName		= 		models.CharField(max_length = 100, null=True)
	Post			=		models.ForeignKey(Post)
	class Meta:
		app_label = 'Insert'

	def __unicode__(self):
		return u'%s %s %s' % (self.userId, self.userName, self.Post)

        

class Comments(models.Model):
	commentId		= 		models.CharField(max_length = 20, null=True)
	userId			= 		models.CharField(max_length = 20, null=True)
	userName		= 		models.CharField(max_length = 100, null=True)
	message			= 		models.CharField(max_length = 10000, null=True)
	created_time	= 		models.CharField(max_length=100, null=True)
	Post			=		models.ForeignKey(Post)
	class Meta:
		app_label = 'Insert'

	def __unicode__(self):
		return u'%s %s %s %s %s %s' % (self.commentId, self.userId, self.userName, self.message, self.created_time, self.Post)






class Message_Tags(models.Model):
	tagId			= 		models.CharField(max_length = 100, null=True)
	tagName			= 		models.CharField(max_length = 100, null=True)
	taggedIdType	=		models.CharField(max_length = 100, null=True)
	Post			=		models.ForeignKey(Post)
	class Meta:
		app_label = 'Insert'

class Place(models.Model):
	PlaceId			=		models.CharField(max_length = 100, null=True)
	Name			=		models.CharField(max_length = 100, null=True)
	City			=		models.CharField(max_length = 100, null=True)
	Country			=		models.CharField(max_length = 100, null=True)
	Street			=		models.CharField(max_length = 100, null=True)
	Longitude		=		models.FloatField()
	Latitude		=		models.FloatField()
	Post			=		models.ForeignKey(Post)
    
	class Meta:
		app_label = 'Insert'
 


