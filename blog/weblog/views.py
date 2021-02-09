from django.shortcuts import render,HttpResponseRedirect,reverse
from .forms import *
from .models import *
from django.contrib.auth.decorators import permission_required,login_required
from django.db import IntegrityError

# Create your views here.
def subtract(queryset,res=''):
    res += f'<li><a href="{queryset.id}" class="text-decoration-none">'+str(queryset)+'</a></li>'
    if queryset.sub_category.all(): res += '<ul class = "list-unstyled">'
    for sub in queryset.sub_category.all():
        res += subtract(sub)
    if queryset.sub_category.all(): res += '</ul>'
    return res

def subtract2(queryset,res):
    res.append(queryset)
    for sub in queryset.sub_category.all():
        res = subtract2(sub,res)
    return res
    
def home(request,category_id=None):
    if category_id:
        title = Category.objects.get(pk=category_id)
        c = subtract2(title,[])
        posts = Post.objects.filter(category__in=c)
    else:
        title = ''
        posts = Post.objects.all()
    Category_html = ''
    for sub in Category.objects.filter(parent=None):
        Category_html += subtract(sub)
    return render(request,'weblog/base.html',{'posts':posts,'category':Category_html, 'title':title})

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

@login_required
def like(request,post_id,value):
    post = Post.objects.get(id=post_id)
    user = request.user
    try:
        Like.objects.create(post=post, user=user, value=bool(value))
    except IntegrityError:
        like = Like.objects.get(post=post,user=user)
        if like.value == value:
            like.delete()
        else:
            like.value=value
            like.save()
    return HttpResponseRedirect(reverse('weblog:home'))