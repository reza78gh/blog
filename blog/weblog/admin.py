from django.contrib import admin, messages
from django.utils.translation import ngettext
from django.contrib.auth.admin import UserAdmin
from .models import *


class CostumeUserAdmin(UserAdmin):
    fieldsets = (
        ('Personal info', {'fields': ('first_name', 'last_name', 'image', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'phone', 'username', 'image', 'password1', 'password2')}
         ),
    )


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'activate', 'accepted']
    actions = ['accept_post', 'active_post']

    def accept_post(self, request, queryset):
        updated = queryset.update(accepted=True)
        self.message_user(request, ngettext(
            '%d پست تایید شد',
            '%d پست تایید شدند',
            updated,
        ) % updated, messages.SUCCESS)

    accept_post.short_description = "تایید کردن"

    def active_post(self, request, queryset):
        updated = queryset.update(activate=True)
        self.message_user(request, ngettext(
            '%d پست فعال شد',
            '%d پست فعال شدند',
            updated,
        ) % updated, messages.SUCCESS)

    active_post.short_description = "فعال کردن"


class CommentAdmin(admin.ModelAdmin):
    list_display = ['text', 'post', 'user', 'accepted']
    actions = ['accept_comment']

    def accept_comment(self, request, queryset):
        updated = queryset.update(accepted=True)
        self.message_user(request, ngettext(
            '%d نظر تایید شد',
            '%d نظر تایید شدند',
            updated,
        ) % updated, messages.SUCCESS)

    accept_comment.short_description = "تایید کردن"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent']


admin.site.register(User, CostumeUserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(Comment, CommentAdmin)
admin.site.register(LikePost)
admin.site.register(LikeComment)
admin.site.register(Category, CategoryAdmin)
