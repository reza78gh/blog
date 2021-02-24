from django import template

register = template.Library()

@register.filter
def count_like(queryset):
    return queryset.filter(value=True).count()

@register.filter    
def count_dislike(queryset):
    return queryset.filter(value=False).count()

@register.filter    
def liked(obj,user):
    return 'btn-danger' if obj.post_like.filter(user=user,value=True) else 'btn-outline-danger'

@register.filter    
def disliked(obj,user):
    return 'btn-secondary' if obj.post_like.filter(user=user,value=False) else 'btn-outline-secondary'

@register.filter    
def comment_liked(obj,user):
    return 'btn-danger' if obj.comment_like.filter(user=user,value=True) else 'btn-outline-danger'

@register.filter    
def comment_disliked(obj,user):
    return 'btn-secondary' if obj.comment_like.filter(user=user,value=False) else 'btn-outline-secondary'