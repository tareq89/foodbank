from django.contrib import admin
from Insert.models import Post, Application, Likes, Comments, Place, Message_Tags

# Register your models here.

admin.site.register(Post)
admin.site.register(Application)
admin.site.register(Likes)
admin.site.register(Comments)
admin.site.register(Place)
admin.site.register(Message_Tags)
