from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.db.models import Q
from comments.forms import CommentForm
from django.contrib.contenttypes.models import ContentType
from comments.models import Comment

# Create your views here.

from comments.models import Comment
from .models import Post

from .forms import PostModelForm

def post_list(request):
    template_name = "list.html"
    query_set_list = Post.objects.all()
    if not request.user.is_staff or not request.user.is_superuser:
        query_set_list = Post.objects.active()

    query = request.GET.get('q')

    if query:
        query_set_list = query_set_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query)
            ).distinct()

    paginator = Paginator(query_set_list, 1)

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
        if object.draft:
            if not request.user.is_staff or not request.user.is_superuser:
                raise Http404
        
        comments = object.comments

        initial_data = {
            "content_type" : object.get_content_type,
            "object_id" : object.id
        }
        comment_form = CommentForm(request.POST or None, initial=initial_data)

        if comment_form.is_valid():
            c_type = comment_form.cleaned_data.get("content_type")
            content_type = ContentType.objects.get(model=c_type)
            obj_id = comment_form.cleaned_data.get("object_id")
            content_data = comment_form.cleaned_data.get("content")
            parent_obj = None
            try:
                parent_id = request.POST.get("parent_id")
            except:
                parent_id = None

            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count() == 1:
                    parent_obj = parent_qs.first()

            new_comment, created = Comment.objects.get_or_create(
                                     user = request.user,
                                     content_type = content_type,
                                     object_id = obj_id,
                                     content = content_data,
                                     parent = parent_obj,
            )
            
            return HttpResponseRedirect(new_comment.content_object.get_absolute_url())


        context = {
            "object"       : object,
            "today"        : timezone.now().date(),
            "comments"     : comments,
            "comment_form" : comment_form
        }
    return render(request, template_name, context)

def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    template_name = "create.html"
    form = PostModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        form = PostModelForm
        messages.success(request, "A post has successfully been created")
    context = {
        'form' : form
    }
    return render(request, template_name, context)

def post_delete(request, id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
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
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    template_name = "update.html"

    instance = get_object_or_404(Post, id=id)
    form = PostModelForm(request.POST or None, request.FILES or None, instance=instance)

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

    

    
        
    