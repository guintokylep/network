from django.contrib import admin

from .models import User, Posts, Profile
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "postUser" , "postDescription" , "likers", "date")

class ProfileAdmin(admin.ModelAdmin):
    list_display = ("userId", "following", "followers")

admin.site.register(User)
admin.site.register(Posts, PostAdmin)
admin.site.register(Profile, ProfileAdmin)
