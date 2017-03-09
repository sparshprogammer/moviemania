from django.contrib import admin
from models import UserProfile, Status_update,Friendship_Request,Movie,Rating,Like,Comment

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Status_update)
admin.site.register(Friendship_Request)
admin.site.register(Movie)
admin.site.register(Rating)
admin.site.register(Like)
admin.site.register(Comment)