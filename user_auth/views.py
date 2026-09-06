import os
import random
import resend

from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db import transaction
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.views.decorators.cache import never_cache
from django.template.loader import render_to_string
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from .models import Profile, Follow
from HOME.models import Blog, Category


User = get_user_model()


# =========================================================
# User Registration Form
# =========================================================

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "form-control"
            })

    def save(self, commit=True):
        user = super().save(commit=False)

        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

        return user


# =========================================================
# Register
# =========================================================

@never_cache
def register_view(request):

    if request.method == "POST":

        form = CustomUserCreationForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            otp_code = str(
                random.randint(100000, 999999)
            )

            request.session["email_verify_otp"] = otp_code
            request.session["email_to_verify"] = user.email
            request.session.set_expiry(600)

            params = {
                "from": "Inkwell Blog <noreply@inkwell.pro.bd>",
                "to": [user.email],
                "subject": "Verify Your Inkwell Email",
                "html": (
                    "<h3>Welcome to Inkwell!</h3>"
                    f"<p>Your verification OTP is: "
                    f"<strong>{otp_code}</strong></p>"
                ),
            }

            try:

                resend.Emails.send(params)

                messages.success(
                    request,
                    "Registration successful! Please verify your email."
                )

                return redirect("verify_email_otp")

            except Exception as e:

                print(f"Resend Error: {e}")

                return redirect("onboarding")

    else:
        form = CustomUserCreationForm()

    return render(
        request,
        "register.html",
        {"form": form}
    )


# =========================================================
# Send Verification OTP
# =========================================================

@login_required(login_url="login")
def send_verification_otp_view(request):

    email = request.user.email

    if not email:

        messages.error(
            request,
            "No email address found in your profile!"
        )

        return redirect("onboarding")

    try:

        validate_email(email)

    except ValidationError:

        messages.error(
            request,
            "Your email address format is invalid! Please update it."
        )

        return redirect("onboarding")

    otp_code = str(
        random.randint(100000, 999999)
    )

    request.session["email_verify_otp"] = otp_code
    request.session["email_to_verify"] = email
    request.session.set_expiry(600)

    params = {
        "from": "Inkwell Blog <noreply@inkwell.pro.bd>",
        "to": [email],
        "subject": "Verify Your Inkwell Account Email",
        "html": f"""
            <h3>Email Verification Code</h3>
            <p>Hello <strong>{request.user.username}</strong>,</p>
            <p>Your OTP for email verification is:
            <strong>{otp_code}</strong></p>
            <p>This code will expire in 10 minutes.</p>
        """,
    }

    try:

        resend.Emails.send(params)

        messages.success(
            request,
            f"A 6-digit verification code has been sent to {email}."
        )

        return redirect("verify_email_otp")

    except Exception as e:

        print(f"Resend Error: {e}")

        messages.error(
            request,
            "Failed to send verification email."
        )

        return redirect("personal")


# =========================================================
# Verify Email OTP
# =========================================================

@login_required(login_url="login")
def verify_email_otp_view(request):

    if request.method == "POST":

        user_otp = request.POST.get(
            "otp",
            ""
        ).strip()

        saved_otp = request.session.get(
            "email_verify_otp"
        )

        if saved_otp and user_otp == saved_otp:

            profile, _ = Profile.objects.get_or_create(
                user=request.user
            )

            profile.is_email_verified = True

            profile.save(
                update_fields=["is_email_verified"]
            )

            request.session.pop(
                "email_verify_otp",
                None
            )

            request.session.pop(
                "email_to_verify",
                None
            )

            messages.success(
                request,
                "Your email address has been verified successfully!"
            )

            return redirect("onboarding")

        else:

            messages.error(
                request,
                "Invalid or expired OTP code!"
            )

    return render(
        request,
        "verify_email_otp.html"
    )


# =========================================================
# Onboarding
# =========================================================

def onboarding_view(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        email = request.POST.get(
            "email",
            ""
        )

        full_name = request.POST.get(
            "full_name",
            ""
        )

        bio = request.POST.get(
            "bio",
            ""
        )

        birthday = (
            request.POST.get("birthday")
            or None
        )

        profile_pic = request.FILES.get(
            "profile_pic"
        )

        request.user.email = email

        request.user.save(
            update_fields=["email"]
        )

        profile.full_name = full_name
        profile.bio = bio
        profile.birthday = birthday

        if profile_pic:

            profile.profile_pic = profile_pic

            print(
                f"Image uploaded: {profile_pic.name}"
            )

        profile.save()

        messages.success(
            request,
            "Profile Edited Successfully!"
        )

        return redirect("personal")

    return render(
        request,
        "onboarding.html",
        {"profile": profile}
    )


# =========================================================
# Login
# =========================================================

@never_cache
def login_view(request):

    if request.method == "POST":

        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            user = form.get_user()

            login(
                request,
                user
            )

            return redirect("personal")

    else:

        form = AuthenticationForm()

    return render(
        request,
        "login.html",
        {"form": form}
    )


# =========================================================
# User Profile
# =========================================================

@login_required(login_url="login")
def profile_view(request):

    posts = (
        Blog.objects
        .select_related(
            "author",
            "author__profile",
            "category",
        )
        .prefetch_related("likes")
        .annotate(
            comment_count=Count(
                "comments",
                distinct=True
            ),
            total_likes=Count(
                "likes",
                distinct=True
            )
        )
        .filter(
            author=request.user
        )
        .order_by("-id")
    )

    # Keep the category queryset behavior unchanged.
    category = (
        Category.objects
        .all()
        .order_by("-id")
    )

    blogs_count = posts.count()

    followers_count = (
        request.user.followers.count()
    )

    search_query = request.GET.get("title")

    if search_query:

        posts = posts.filter(
            title__icontains=search_query
        )

    paginator = Paginator(
        posts,
        6
    )

    page_num = request.GET.get("page")

    paginated_posts = paginator.get_page(
        page_num
    )

    context = {
        "blogs_count": blogs_count,
        "posts": paginated_posts,
        "category": category,
        "followers_count": followers_count,
    }

    profile, _ = Profile.objects.get_or_create(
        user=request.user
    )

    if not request.user.email:

        messages.warning(
            request,
            "Please add a valid email address to your profile!"
        )

    elif not profile.is_email_verified:

        messages.warning(
            request,
            "Your email is not verified yet! Please verify your email to secure your account."
        )

    return render(
        request,
        "personal.html",
        context
    )


# =========================================================
# Logout
# =========================================================

def logout_view(request):

    if request.method == "POST":

        logout(request)

        return redirect("login")

    return redirect("personal")


# =========================================================
# Create Post
# =========================================================

@login_required(login_url="login")
def create_post(request):

    if request.method == "POST":

        title = request.POST.get("title")
        image = request.FILES.get("image")
        content = request.POST.get("content")
        category_id = request.POST.get("category")

        status = "1"
        section = "Recent"

        if request.user.is_staff:

            status = request.POST.get("status")
            section = request.POST.get("section")

        Blog.objects.create(
            title=title,
            author=request.user,
            image=image,
            content=content,
            category_id=category_id,
            status=status,
            section=section,
        )

        messages.success(
            request,
            "Post created successfully!"
        )

        return redirect("index")

    categories = Category.objects.all()

    return render(
        request,
        "create.html",
        {"categories": categories}
    )


# =========================================================
# Edit Post
# =========================================================

def edit_post(request, slug):

    post = get_object_or_404(
        Blog,
        blog_slug=slug
    )

    if (
        post.author != request.user
        and not request.user.is_staff
    ):

        messages.error(
            request,
            "You are not authorized to edit this post."
        )

        return redirect("index")

    if request.method == "POST":

        post.title = request.POST.get(
            "title"
        )

        post.content = request.POST.get(
            "content"
        )

        category_id = request.POST.get(
            "category"
        )

        if category_id:

            post.category = get_object_or_404(
                Category,
                id=category_id
            )

        if request.FILES.get("image"):

            post.image = request.FILES.get(
                "image"
            )

        post.save()

        messages.success(
            request,
            "Post edited successfully!"
        )

        return redirect("personal")

    categories = Category.objects.all()

    data = {
        "post": post,
        "categories": categories,
    }

    return render(
        request,
        "editpost.html",
        data
    )


# =========================================================
# Delete Post
# =========================================================

def delete_post(request, slug):

    post = Blog.objects.get(
        blog_slug=slug
    )

    post.delete()

    messages.error(
        request,
        "Post deleted!"
    )

    return redirect("personal")


# =========================================================
# Add Category
# =========================================================

def add_category(request):

    if request.method == "POST":

        name = request.POST.get(
            "name"
        )

        Category.objects.create(
            name=name
        )

        return redirect("create_post")

    return redirect("create_post")


# =========================================================
# Author Profile
# =========================================================

def author_profile(request, username):

    author_name = get_object_or_404(
        User,
        username=username
    )

    posts = (
        Blog.objects
        .select_related(
            "author",
            "author__profile",
            "category",
        )
        .prefetch_related("likes")
        .annotate(
            comment_count=Count(
                "comments",
                distinct=True
            ),
            total_likes=Count(
                "likes",
                distinct=True
            )
        )
        .filter(
            author=author_name
        )
        .order_by("-id")
    )

    category = (
        Category.objects
        .all()
        .order_by("-id")
    )

    is_following = False

    if request.user.is_authenticated:

        is_following = Follow.objects.filter(
            follower=request.user,
            following=author_name
        ).exists()

    followers_count = (
        author_name.followers.count()
    )

    blogs_count = posts.count()

    search_query = request.GET.get(
        "title"
    )

    if search_query:

        posts = posts.filter(
            title__icontains=search_query
        )

    paginator = Paginator(
        posts,
        6
    )

    page_num = request.GET.get(
        "page"
    )

    paginated_posts = paginator.get_page(
        page_num
    )

    context = {
        "author_name": author_name,
        "posts": paginated_posts,
        "blogs_count": blogs_count,
        "category": category,
        "is_following": is_following,
        "followers_count": followers_count,
    }

    return render(
        request,
        "author_profile.html",
        context
    )


# =========================================================
# Follow
# =========================================================

@login_required(login_url="login")
def toggle_follow(request, user_id):

    if request.method != "POST":

        return HttpResponseNotAllowed(
            ["POST"]
        )

    target_user = get_object_or_404(
        User,
        id=user_id
    )

    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        following=target_user
    )

    if not created:

        follow.delete()

        return JsonResponse({
            "status": "unfollowed"
        })

    return JsonResponse({
        "status": "following"
    })


# =========================================================
# Password Reset
# =========================================================

resend.api_key = getattr(
    settings,
    "RESEND_API_KEY",
    None
)


# =========================================================
# Password Reset - Send OTP
# =========================================================

def password_reset_view(request):

    if request.method == "POST":

        email = request.POST.get(
            "email",
            ""
        ).strip()

        # One query instead of exists() + first()
        user = (
            User.objects
            .filter(
                email__iexact=email
            )
            .first()
        )

        if not user:

            messages.error(
                request,
                "This email address is not registered!"
            )

            return render(
                request,
                "password_reset_form.html"
            )

        otp_code = str(
            random.randint(100000, 999999)
        )

        request.session["generated_otp"] = otp_code
        request.session["otp_email"] = email
        request.session.set_expiry(300)

        html_content = render_to_string(
            "email/otp_template.html",
            {
                "username": user.username,
                "otp": otp_code,
            }
        )

        params = {
            "from": "Inkwell Blog <noreply@inkwell.pro.bd>",
            "to": [email],
            "subject": "Your Inkwell Password Reset OTP",
            "html": html_content,
        }

        try:

            resend.Emails.send(params)

            messages.success(
                request,
                "A 6-digit OTP has been sent to your email."
            )

            return redirect(
                "password_reset_done"
            )

        except Exception as e:

            print(
                f"Resend Error: {e}"
            )

            messages.error(
                request,
                "Failed to send email."
            )

    return render(
        request,
        "password_reset_form.html"
    )


# =========================================================
# Password Reset - Verify OTP
# =========================================================

def password_reset_done_view(request):

    if request.method == "POST":

        user_otp = request.POST.get(
            "otp"
        )

        saved_otp = request.session.get(
            "generated_otp"
        )

        if saved_otp and user_otp == saved_otp:

            request.session["otp_verified"] = True

            request.session.pop(
                "generated_otp",
                None
            )

            return redirect(
                "password_reset_confirm"
            )

        else:

            messages.error(
                request,
                "Invalid or expired OTP!"
            )

    return render(
        request,
        "password_reset_done.html"
    )


# =========================================================
# Password Reset - Confirm
# =========================================================

def password_reset_confirm_view(request):

    if not request.session.get(
        "otp_verified"
    ):

        messages.error(
            request,
            "Please verify your OTP first."
        )

        return redirect(
            "password_reset"
        )

    if request.method == "POST":

        password = request.POST.get(
            "password"
        )

        confirm_password = request.POST.get(
            "confirm_password"
        )

        email = request.session.get(
            "otp_email"
        )

        if password != confirm_password:

            messages.error(
                request,
                "Passwords do not match!"
            )

            return render(
                request,
                "password_reset_confirm.html"
            )

        try:

            user = User.objects.get(
                email=email
            )

            user.password = make_password(
                password
            )

            user.save(
                update_fields=["password"]
            )

            request.session.pop(
                "otp_email",
                None
            )

            request.session.pop(
                "otp_verified",
                None
            )

            return redirect(
                "password_reset_complete"
            )

        except Exception:

            messages.error(
                request,
                "Something went wrong. Please try again."
            )

    return render(
        request,
        "password_reset_confirm.html"
    )


# =========================================================
# Password Reset - Complete
# =========================================================

def password_reset_complete_view(request):

    return render(
        request,
        "password_reset_complete.html"
    )