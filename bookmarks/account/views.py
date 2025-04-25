from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse

from actions.utils import create_action
from actions.models import Action
from .forms import (
    UserRegistrationForm,
    LoginForm,
    UserEditForm,
    ProfileEditForm
)
from .models import Profile, Contact


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


@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(
                    user_from=request.user,
                    user_to=user
                )
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(
                    user_from=request.user,
                    user_to=user
                ).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})
    

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
            create_action(new_user, 'has created an account')
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
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list(
        'id', flat=True
    )
    if following_ids:
        actions = actions.filter(user_id__in=following_ids)
    actions = actions.select_related(
        'user', 'user__profile'   
    ).prefetch_related('target')[:10]
    return render(
        request,
        template_name='account/dashboard.html',
        context={
            'section': 'dashboard',
            'actions': actions
        }
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
    