from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.register(User,UserAdmin)
admin.site.unregister(User)
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(LikePost)
admin.site.register(LikeComment)
admin.site.register(Category)
