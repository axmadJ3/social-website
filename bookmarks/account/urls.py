from django.urls import path
from django.contrib.auth import views as builtin_views

from . import views


urlpatterns = [
    # path('login/', views.user_login, name='login'),
    path('login/', builtin_views.LoginView.as_view(), name='login'),
    path('logout/', builtin_views.LogoutView.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),
]
