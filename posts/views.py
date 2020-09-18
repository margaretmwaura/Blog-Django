from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
# Create your views here.

from .models import Post

def post_list(request):
    template_name = "index.html"
    query_set = Post.objects.all()
    context = {
        "object_list" : query_set
    }
    return render(request, template_name, context)

def post_detail(request, id=None):
    template_name = "detail.html"
    print(id)
    if id is not None:
        object = get_object_or_404(Post, id=id)
        context = {
            "object" : object
        }
    return render(request, template_name, context)

    
        
    