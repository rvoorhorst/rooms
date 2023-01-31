from django.contrib import admin

from apps.base.models import Comment, Message, Profile, Room, Topic

admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(Message)
