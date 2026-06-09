from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Club
from .forms import ClubForm, ClubFilterForm


class clubsView(TemplateView):
    template_name = 'clubs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clubs = Club.objects.filter(is_approved=True)

        filter_form = ClubFilterForm(self.request.GET)
        if filter_form.is_valid():
            name = filter_form.cleaned_data.get('name')
            if name:
                clubs = clubs.filter(name__icontains=name)

        context['clubs'] = clubs
        context['filter_form'] = filter_form
        return context


@login_required
def club_detail(request, pk):
    club = get_object_or_404(Club, id=pk, is_approved=True)
    is_member = club.members.filter(id=request.user.id).exists()
    context = {
        'club': club,
        'is_member': is_member,
    }
    return render(request, 'club_detail.html', context)


@login_required
def create_club(request):
    if request.user.role not in ['club_manager', 'admin']:
        return HttpResponseForbidden('Only club managers can create clubs.')
    if request.method == 'POST':
        form = ClubForm(request.POST, request.FILES)
        if form.is_valid():
            club = form.save(commit=False)
            club.owner = request.user
            club.is_approved = False
            club.save()
            if request.user.role == 'admin':
                return redirect('admin_dashboard')
            return redirect('manager_dashboard')
    else:
        form = ClubForm()
    return render(request, 'club_form.html', {'form': form})


@login_required
def edit_club(request, pk):
    club = get_object_or_404(Club, id=pk)
    if club.owner != request.user and request.user.role != 'admin':
        return HttpResponseForbidden('You can only edit your own clubs.')
    if request.method == 'POST':
        form = ClubForm(request.POST, request.FILES, instance=club)
        if form.is_valid():
            form.save()
            return redirect('club_detail', pk=pk)
    else:
        form = ClubForm(instance=club)
    return render(request, 'club_form.html', {'form': form, 'edit': True})


@login_required
def delete_club(request, pk):
    club = get_object_or_404(Club, id=pk)
    if club.owner != request.user and request.user.role != 'admin':
        return HttpResponseForbidden('Access denied.')
    club.delete()
    return redirect('clubs')


@login_required
def join_club(request, pk):
    club = get_object_or_404(Club, id=pk, is_approved=True)
    club.members.add(request.user)
    return redirect('club_detail', pk=pk)


@login_required
def leave_club(request, pk):
    club = get_object_or_404(Club, id=pk)
    club.members.remove(request.user)
    return redirect('club_detail', pk=pk)


@login_required
def approve_club(request, pk):
    if request.user.role != 'admin':
        return HttpResponseForbidden('Access denied.')
    club = get_object_or_404(Club, id=pk)
    club.is_approved = True
    club.save()
    return redirect('admin_dashboard')


@login_required
def reject_club(request, pk):
    if request.user.role != 'admin':
        return HttpResponseForbidden('Access denied.')
    club = get_object_or_404(Club, id=pk)
    club.delete()
    return redirect('admin_dashboard')


@login_required
def club_members(request, pk):
    club = get_object_or_404(Club, id=pk)
    if club.owner != request.user and request.user.role != 'admin':
        return HttpResponseForbidden('Access denied.')
    members = club.members.all()
    return render(request, 'club_members.html', {'club': club, 'members': members})