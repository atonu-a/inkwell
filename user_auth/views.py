from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Profile
from HOME.models import Blog, Category
from django.core.paginator import Paginator
from django.contrib.auth.models import User

# Create your views here.


def register_view(request):
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('onboarding')  
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form':form})

def onboarding_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        full_name = request.POST.get("full_name", "")
        bio = request.POST.get("bio", "")
        birthday = request.POST.get("birthday") or None
        profile_pic = request.FILES.get('profile_pic')     
        profile.full_name = full_name
        profile.bio = bio
        profile.birthday = birthday
        if profile_pic: 
            profile.profile_pic = profile_pic
            print(f"Image uploaded: {profile_pic.name}")
        profile.save()
        return redirect('personal')
    return render(request, 'onboarding.html', {'profile': profile})       
            
    
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('personal')
    else:
        form = AuthenticationForm()
            
    return render(request, 'login.html',  {'form':form})


@login_required(login_url='login')
def profile_view(request):
    posts = Blog.objects.annotate(comment_count=Count('comments')).filter(author=request.user).order_by("-id")
    category = Category.objects.all().order_by("-id")
    blogs_count = posts.count()
    
    search_query = request.GET.get("title")
    if search_query :
        posts = posts.filter(title__icontains= search_query)
        
    paginator = Paginator(posts,6)
    page_num = request.GET.get('page')
    paginated_posts = paginator.get_page(page_num)
    
    
    context = {

        "blogs_count":blogs_count,
        "posts" : paginated_posts,
        "category" : category
        
    }
    
    return render(request, "personal.html", context)


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')
    return redirect("personal")

@login_required(login_url='login')
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        image = request.FILES.get('image')
        content = request.POST.get('content')
        category_id = request.POST.get('category')
        status = "1"
        section = "Recent"
        if request.user.is_staff:
            status = request.POST.get("status")
            section = request.POST.get("section")
        
        
        category = Category.objects.get(id=category_id)
        
        Blog.objects.create(
            title=title,
            author = request.user,
            image=image,
            content=content,
            category=category,
            status=status,
            section=section
        )
        return redirect('index')
    
    categories =  Category.objects.all()

        
    
    return render(request,"create.html",{"categories": categories})

def delete_post(request, slug):
    post = Blog.objects.get(blog_slug = slug)
    post.delete()
    return redirect("personal")

def add_category(request):
    if request.method == "POST":
        name = request.POST.get("name")
        Category.objects.create(
            name = name
        )
        return redirect("create_post")
    return redirect("create_post")

def author_profile(request, username):
    author_name = get_object_or_404(User, username=username)
    posts = Blog.objects.annotate(comment_count=Count('comments')).filter(author=author_name).order_by("-id")
    category = Category.objects.all().order_by("-id")
    
    blogs_count = posts.count()
    
    search_query = request.GET.get("title")
    if search_query :
        posts = posts.filter(title__icontains= search_query)
        
    paginator = Paginator(posts,6)
    page_num = request.GET.get('page')
    paginated_posts = paginator.get_page(page_num)
    context = {
        'author_name': author_name,
        'posts': paginated_posts,
        'blogs_count' : blogs_count,
        'category' : category
    }
    return render(request, 'author_profile.html', context)
        