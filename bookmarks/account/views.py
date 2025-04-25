from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .forms import (
    UserRegistrationForm,
    LoginForm,
    UserEditForm,
    ProfileEditForm
)
from .models import Profile


User = get_user_model()


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(
        request,
        template_name='account/user/list.html',
        context={
            'section': 'people',
            'users': users
        }
    )
    
    
@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(
        request,
        template_name='account/user/detail.html',
        context={
            'section': 'people',
            'user': user
        }
    )


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(
                request,
                template_name='account/register_done.html',
                context={'new_user': new_user}
            )
    else:
        user_form = UserRegistrationForm()
    return render(
        request,
        template_name='account/register.html',
        context={'user_form': user_form}
    )


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password']
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(
        request, 
        template_name='account/login.html', 
        context={'form': form}
    )


@login_required
def dashboard(request):
    return render(
        request,
        template_name='account/dashboard.html',
        context={'section': 'dashboard'}
    )


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(
            instance=request.user,
            data=request.POST
        )
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(
                request,
                'Profile updated successfully'
            )
        else:
            messages.error(
                request,
                'Error updating your profile'
            )
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
        request,
        template_name='account/edit.html',
        context={
            'user_form': user_form, 
            'profile_form': profile_form
        }
    )
    