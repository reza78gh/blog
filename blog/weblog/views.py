from django.shortcuts import render,HttpResponseRedirect,reverse
from .forms import *
from .models import *
from django.contrib.auth.decorators import permission_required,login_required
from django.db import IntegrityError
from django.views import generic
import requests
import re
from bs4 import BeautifulSoup
# Create your views here.

def subtract2(queryset,res):
    res.append(queryset)
    for sub in queryset.sub_category.all():
        res = subtract2(sub,res)
    return res
    
def home(request,pk=None,mode=None):
    if mode == 'category':
        title = Category.objects.get(pk=pk)
        c = subtract2(title,[])
        posts = Post.objects.filter(accepted=True,activate=True,category__in=c)
    elif mode == 'tag':
        title = Tag.objects.get(pk=pk)
        posts = Post.objects.filter(accepted=True,activate=True,tag=title)
    else:
        title = ''
        posts = Post.objects.filter(accepted=True,activate=True,)
    return render(request,'weblog/base.html',{'posts':posts, 'title':title})

@permission_required("weblog.can_write")
def new_post(request):
    if request.POST:
        form = NewPost(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            post.tag.set([Tag.objects.get_or_create(name=i)[0] for i in request.POST.getlist('tags') if i])
            return HttpResponseRedirect(reverse('weblog:detail_post', args=(post.id,)))
    else:
        form = NewPost()
    tags = Tag.objects.all()
    return render(request,"weblog/new_post.html",{'form':form,'tags':tags})

def register(request):
    if request.POST:
        form = NewUserForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('weblog:home'))
    else:
        form = NewUserForm()
    return render(request,'weblog/register.html',{'form':form})


class DetailPostView(generic.DetailView):
    model = Post
    template_name = 'weblog/detail_post.html'
        
    def get_context_data(self, **kwargs):          
        context = super().get_context_data(**kwargs)                     
        context['comment_form'] = CommentForm()
        return context
    
    
def search(request):
    if request.POST:
        r = requests.get('http://127.0.0.1:8000/')
        soup = BeautifulSoup(r.content, 'html.parser')
        all_posts = soup.find_all('div',{'class':'col'})
        if request.POST['mode'] == 'normal':
            posts = [i['id'] for i in all_posts if i.find_all(text=re.compile(request.POST['search']))]
            mypost = Post.objects.filter(id__in=posts)
        elif request.POST['mode'] == 'advance':
            posts = set()
            if request.POST['title']:
                title = {i['id'] for i in all_posts if i.find('h3').find_all(text=re.compile(request.POST['title']))}
                posts = posts&title if posts else title
            if request.POST['text']:
                text = {i['id'] for i in all_posts if i.find('p',{'class':'card-text'}).find_all(text=re.compile(request.POST['text']))}
                posts = posts&text if posts else text
            if request.POST['author']:
                author = {i['id'] for i in all_posts if i.find('p',{'id':'author'}).find_all(text=re.compile(request.POST['author']))}
                posts = posts&author if posts else author
            if request.POST['tag']:
                tag = {i['id'] for i in all_posts if i.find('div',{'id':'tags'}).find_all(text=re.compile(request.POST['tag']))}
                posts = posts&tag if posts else tag
            mypost = Post.objects.filter(id__in=posts)
        return render(request,'weblog/base.html',{'posts':mypost})