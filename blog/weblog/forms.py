from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Post, User, Comment

class NewPost(ModelForm):
    class Meta:
        model = Post
        fields = ['title','text','img','activate','category']
        

class NewUserForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ['first_name','last_name','phone','image','username']        

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']