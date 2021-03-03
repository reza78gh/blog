from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

class User(AbstractUser):
    class Meta:
        permissions = [('can_write','can write post'),
                       ('can_edit','can accept and edit other posts and comments'),
                       ('can_manage','can manage all content and users')]
    phone = models.BigIntegerField("شماره",null=True)
    image = models.ImageField("تصویر", upload_to='users',null=True)
    
    
class Post(models.Model):
    title = models.CharField("عنوان",max_length=70)
    text = models.TextField("متن")
    img = models.ImageField(upload_to='posts')
    created_time = models.DateTimeField("تاریخ ایجاد",auto_now_add=True)
    activate = models.BooleanField("فعال",default=True)
    accepted = models.BooleanField("تایید",default=False)
    tag = models.ManyToManyField("Tag",related_name="tag_post",verbose_name="تگ ها")
    author = models.ForeignKey("User", verbose_name="نویسنده",related_name='author_post' ,on_delete=models.CASCADE)
    category = models.ForeignKey("Category",verbose_name="دسته بندی",on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    
    
class Comment(models.Model):
    post = models.ForeignKey("Post", verbose_name="پست",related_name='post_comment', on_delete=models.CASCADE)
    text = models.TextField("متن")
    accepted = models.BooleanField("تایید",default=False)
    user = models.ForeignKey("User", verbose_name="کاربر",related_name='user_comment', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.text[:50] + '...'
    
    
class Like(models.Model):
    class Meta:
        abstract = True
    value = models.BooleanField("لایک؟",default=True)
    user = models.ForeignKey("User", verbose_name="کاربر",related_name='user_%(class)s', on_delete=models.CASCADE)
    
    def __str__(self):
        return 'like' if self.value else 'dislike'
    
class LikePost(Like):
    class Meta:
        unique_together = [['post', 'user']]
    post = models.ForeignKey("Post", verbose_name="پست",related_name='post_like', on_delete=models.CASCADE)
    
class LikeComment(Like):
    class Meta:
        unique_together = [['comment', 'user']]
    comment = models.ForeignKey('Comment',verbose_name="کامنت",related_name='comment_like',on_delete=models.CASCADE)
    
    
class Tag(models.Model):
    name = models.CharField("نام",max_length=70)
    
    def __str__(self):
        return self.name
    
    
class Category(models.Model):
    name = models.CharField("نام",max_length=30)
    parent = models.ForeignKey('Category',related_name="sub_category",null=True,blank=True,on_delete=models.SET_NULL)
    
    def __str__(self):
        return self.name