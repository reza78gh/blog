from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Post, User

class NewPost(ModelForm):
    class Meta:
        model = Post
        fields = ['title','text','img','activate','tag','category']
        

class NewUserForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ['first_name','last_name','phone','image','username']