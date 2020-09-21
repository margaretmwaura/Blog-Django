from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

from .models import Post

from .forms import PostModelForm

def post_list(request):
    template_name = "list.html"
    query_set_list = Post.objects.all()
    paginator = Paginator(query_set_list, 5)

    page = request.GET.get('page')
    try:
        query_set = paginator.page(page)
    except PageNotAnInteger:
        query_set = paginator.page(1)
    except EmptyPage:
        query_set = paginator.page(paginator.num_pages)

    context = {
        "object_list" : query_set
    }
    return render(request, template_name, context)

def post_detail(request, id=None):
    template_name = "detail.html"
    if id is not None:
        object = get_object_or_404(Post, id=id)
        context = {
            "object" : object
        }
    return render(request, template_name, context)

def post_create(request):
    template_name = "create.html"
    form = PostModelForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = PostModelForm
        messages.success(request, "A post has successfully been created")
    context = {
        'form' : form
    }
    return render(request, template_name, context)

def post_delete(request, id=None):
    post = get_object_or_404(Post, id=id)
    template_name = "delete.html"
    if request.method == "POST":
        post.delete()
        return redirect("posts:list")
    context = {
       'obj' : post
    }
    return render(request, template_name, context)

def post_update(request, id=None):
    template_name = "update.html"

    instance = get_object_or_404(Post, id=id)
    form = PostModelForm(request.POST or None, instance=instance)

    if form.is_valid():
        form.save()
        messages.success(request, "A post has successfully been editted")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "The post was not editted")
    context = {
        "form" : form,
        "obj" : instance
    }
    return render(request, template_name, context)

    

    
        
    