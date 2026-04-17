from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from .models import *
from django.core.paginator import Paginator
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Create your views here.

def index(request):
    posts = Blog.objects.annotate(comment_count=Count('comments')).order_by("?")
    main_post = Blog.objects.filter(section="Main_Post").order_by("-id")[:1]
    recent = Blog.objects.all().order_by("-date")
    popular = Blog.objects.annotate(like_count=Count('likes')).order_by('-like_count')
    trending = Blog.objects.annotate(like_count=Count('likes')).order_by('-like_count')[:2]
    category = Category.objects.annotate(count=Count('blog'))

    context = {       
        'posts' : posts,
        'main_post' : main_post,
        'recent' : recent,
        'category': category,
        'popular': popular,
        'trending_left': trending[:1],
        'trending_right': trending[1:2],
        
        
               
    }
    return render(request,"index.html", context)

def blog_detail(request,slug):
    
    category = Category.objects.annotate(count=Count('blog'))
    post = get_object_or_404(Blog, blog_slug = slug)
    comments = Comment.objects.filter(blog_id  = post.id).order_by("-date")
    context = {       
        'category': category,
        'post' : post,
        'comments': comments
               
    }
    return render(request, "blog-single.html", context)
def category(request, slug):
    category = Category.objects.annotate(count=Count('blog')).order_by("-id")
    current_category = get_object_or_404(Category, slug=slug)
    blog_category = Category.objects.filter(slug=slug)
    blog_posts = current_category.blog.all()
    
    search_query = request.GET.get("title")
    if search_query :
        blog_posts = blog_posts.filter(title__icontains= search_query)
        
    paginator = Paginator(blog_posts,4)
    page_num = request.GET.get('page')
    paginated_posts = paginator.get_page(page_num)
    
    
    
    context = {
        "category":category,
        "current_category":current_category,
        "blog_posts":paginated_posts,
        "active_category": slug,
        "blog_category" : blog_category,
        "total_pages": paginator.num_pages,
        "search_query" : search_query or "",
        
    }
    return render(request, "category.html",context)

def profile_view(request):
    return render(request, "personal.html")

@login_required(login_url="login")
def like_view(request, slug):
    post = get_object_or_404(Blog, blog_slug = slug)
    liked = False
    
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False

    else:
        post.likes.add(request.user)
        liked = True

        
    return JsonResponse({
        "liked":liked,
        "total_likes" : post.total_likes()
    })

from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog, Comment

def add_comment(request, slug):
    if request.method == "POST":
        post = get_object_or_404(Blog, blog_slug=slug)
        comment_text = request.POST.get("InputComment")
        parent_id = request.POST.get("parent_id")
        

        if request.user.is_authenticated:
            user_obj = request.user
        else:

            return redirect("login")

        parent_comment = None
        if parent_id:
            parent_comment = Comment.objects.get(id=parent_id)

        Comment.objects.create(
            post=post,
            comment=comment_text,
            name=user_obj,
            parent=parent_comment
        )
        
        return redirect("blog_detail", slug=post.blog_slug)
    
    return redirect("index")
@login_required(login_url='login')
def delete_comment(request, id):

    comment = get_object_or_404(Comment, id=id)

    if comment.name == request.user or request.user.is_staff:
        post_slug = comment.post.blog_slug
        comment.delete()
        return redirect('blog_detail', slug=post_slug)
    else:

        return redirect('index')
