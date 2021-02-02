from django.shortcuts import render
from .forms import *
from .models import *

# Create your views here.
def home(request):
    posts = Post.objects.all()
    # print(list(Post.tag.all()))
    return render(request,'weblog/base.html',{'posts':posts})


def new_post(request):
    if request.POST:
        form = NewPost(request.POST,request.FILES)
        print("ok welldown",request.user)
        if form.is_valid():
            print(form.cleaned_data)
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            post.save_m2m()
    else:
        form = NewPost()
    return render(request,"weblog/new_post.html",{'form':form})
