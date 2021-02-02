from django.forms import ModelForm
from .models import Post

class NewPost(ModelForm):
    class Meta:
        model = Post
        fields = ['title','text','img','activate','tag','category']
        