from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import SignUpForm, ProfileEditForm, UserRoleForm
from .models import CustomUser
from Club.models import Club
from Event.models import Event


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def profile_view(request):
    return render(request, 'profile.html')


@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})


@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return HttpResponseForbidden('Access denied.')
    pending_clubs = Club.objects.filter(is_approved=False)
    all_clubs = Club.objects.all()
    all_users = CustomUser.objects.exclude(id=request.user.id)
    all_events = Event.objects.all().order_by('-created_at')
    context = {
        'pending_clubs': pending_clubs,
        'all_clubs': all_clubs,
        'all_users': all_users,
        'all_events': all_events,
    }
    return render(request, 'admin_dashboard.html', context)


@login_required
def change_user_role(request, pk):
    if request.user.role != 'admin':
        return HttpResponseForbidden('Access denied.')
    user = get_object_or_404(CustomUser, id=pk)
    if request.method == 'POST':
        form = UserRoleForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = UserRoleForm(instance=user)
    return render(request, 'change_role.html', {'form': form, 'target_user': user})


@login_required
def delete_user(request, pk):
    if request.user.role != 'admin':
        return HttpResponseForbidden('Access denied.')
    user = get_object_or_404(CustomUser, id=pk)
    user.delete()
    return redirect('admin_dashboard')


@login_required
def manager_dashboard(request):
    if request.user.role != 'club_manager':
        return HttpResponseForbidden('Access denied.')
    my_clubs = Club.objects.filter(owner=request.user)
    my_events = Event.objects.filter(created_by=request.user).order_by('-created_at')
    context = {
        'my_clubs': my_clubs,
        'my_events': my_events,
    }
    return render(request, 'manager_dashboard.html', context)