from django.shortcuts import render,HttpResponseRedirect,reverse
from .forms import *
from .models import *
from django.contrib.auth.decorators import permission_required,login_required

# Create your views here.
def home(request):
    posts = Post.objects.all()
    return render(request,'weblog/base.html',{'posts':posts})

@permission_required("weblog.can_write")
def new_post(request):
    if request.POST:
        form = NewPost(request.POST,request.FILES)
        print("ok welldown",request.user)
        if form.is_valid():
            print(form.cleaned_data)
            post = form.save(commit=False)
            post.author = request.user
            post.save()
    else:
        form = NewPost()
    return render(request,"weblog/new_post.html",{'form':form})

def register(request):
    if request.POST:
        form = NewUserForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('weblog:home'))
    else:
        form = NewUserForm()
    return render(request,'weblog/register.html',{'form':form})


@login_required
def add_comment(request,post_id):
    if request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(text=form.cleaned_data['text'],
                                   post=Post.objects.get(id=post_id),
                                   user=request.user)
            return HttpResponseRedirect(reverse('weblog:home'))
    else:
        form = CommentForm()
    return render(request,'weblog/add_comment.html',{'form':form, 'post_id':post_id})