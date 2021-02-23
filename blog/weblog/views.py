from django.shortcuts import render,HttpResponseRedirect,reverse
from .forms import *
from .models import *
from django.contrib.auth.decorators import permission_required,login_required
from django.db import IntegrityError
from django.views import generic

# Create your views here.
def subtract(queryset,res=''):
    href = '{% url "weblog:category" '+str(queryset)+' %}'
    res += f'<li><a href="{href}" class="text-decoration-none">'+str(queryset)+'</a></li>'
    if queryset.sub_category.all(): res += '<ul>'
    for sub in queryset.sub_category.all():
        res += subtract(sub)
    if queryset.sub_category.all(): res += '</ul>'
    return res

def subtract2(queryset,res):
    res.append(queryset)
    for sub in queryset.sub_category.all():
        res = subtract2(sub,res)
    return res
    
def home(request,pk=None,mode=None):
    print(mode)
    if mode == 'category':
        title = Category.objects.get(pk=pk)
        c = subtract2(title,[])
        posts = Post.objects.filter(category__in=c)
    elif mode == 'tag':
        title = Tag.objects.get(pk=pk)
        posts = Post.objects.filter(tag=title)
    else:
        title = ''
        posts = Post.objects.all()
    Category_html = '<div class="d-flex">'
    for sub in Category.objects.filter(parent=None):
        Category_html += f'<div class="me-5">{subtract(sub)}</div>'  
    Category_html += '</div>'
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
            post.tag.set(Tag.objects.filter(name__in=request.POST.getlist('tags')))
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


class DetailPostView(generic.DetailView):
    model = Post
    template_name = 'weblog/detail_post.html'
    
    # def get(self, request, *args, **kwargs):
    #     context = locals()
    #     context['comment_form'] = CommentForm()
    #     return render_to_response(self.response_template, context, context_instance=RequestContext(request))
    
    def get_context_data(self, **kwargs):          
        context = super().get_context_data(**kwargs)                     
        context['comment_form'] = CommentForm()
        return context