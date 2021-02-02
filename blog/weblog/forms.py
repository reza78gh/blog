from django.forms import ModelForm
from .models import Post, User

class NewPost(ModelForm):
    class Meta:
        model = Post
        fields = ['title','text','img','activate','tag','category']
        
class NewUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','phone','image','username','password']