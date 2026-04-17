from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('login/', views.login_view , name="login"),
    path('add-category/', views.add_category, name="add_category"),
    path("profile/<str:username>", views.author_profile, name="author_profile"),
    path('register/', views.register_view, name="register_view"),
    path('logout/', views.logout_view, name="logout_view"),
    path('onboarding/', views.onboarding_view, name='onboarding'),
    path("create-post/", views.create_post, name="create_post"),
    path("delete-post/<slug:slug>/", views.delete_post, name = "delete_post"),
    path('profile/', views.profile_view, name="personal"),
    
    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    