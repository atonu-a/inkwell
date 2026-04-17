from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path("category/<str:slug>/", views.category, name="category"),
    path("<str:slug>/", views.blog_detail, name = 'blog_detail'),  
    path("like/<slug:slug>/", views.like_view, name="like"),
    path("<slug:slug>/add_comment/", views.add_comment, name="add_comment"),
    path('delete-comment/<int:id>/', views.delete_comment, name='delete_comment'),
    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    