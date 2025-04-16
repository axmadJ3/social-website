from django.urls import path, include
from django.contrib.auth import views as builtin_views

from . import views


urlpatterns = [
    # path('login/', views.user_login, name='login'),
    # path('login/', 
    #      builtin_views.LoginView.as_view(), 
    #      name='login'),
    # path('logout/', 
    #      builtin_views.LogoutView.as_view(), 
    #      name='logout'),
    # path(
    #     'password-change/', 
    #     builtin_views.PasswordChangeView.as_view(), 
    #     name='password_change'),
    # path(
    #     'password-change/done/', 
    #     builtin_views.PasswordChangeDoneView.as_view(), 
    #     name='password_change_done'),
    # path(
    #     'password-reset/',
    #     builtin_views.PasswordResetView.as_view(),
    #     name='password_reset'
    # ),
    # path(
    #     'password-reset/done/',
    #     builtin_views.PasswordResetDoneView.as_view(),
    #     name='password_reset_done'
    # ),
    # path(
    #     'password-reset/<uidb64>/<token>/',
    #     builtin_views.PasswordResetConfirmView.as_view(),
    #     name='password_reset_confirm'
    # ),
    # path(
    #     'password-reset/complete',
    #     builtin_views.PasswordResetCompleteView.as_view(),
    #     name='password_reset_complite'
    # ),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    
    path('', include('django.contrib.auth.urls')),
    path('', views.dashboard, name='dashboard'),
]
