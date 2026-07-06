from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
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
    path('follow/<int:user_id>/', views.toggle_follow, name='toggle_follow'),
    path('edit-post/<slug:slug>/', views.edit_post, name="edit_post"),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    
    
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]