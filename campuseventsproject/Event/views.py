from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden
from .models import Event, EventRegistration
from .forms import EventForm
from Club.models import Club


class eventsView(TemplateView):
    template_name = 'events.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        club_id = self.kwargs.get('club_id')
        events = Event.objects.filter(club__is_approved=True).order_by('date')

        if club_id:
            events = events.filter(club__id=club_id)
            context['club'] = Club.objects.filter(id=club_id).first()
        else:
            context['club'] = None

        context['events'] = events
        return context


@login_required
def create_event(request):
    if request.user.role not in ['club_manager', 'admin']:
        return HttpResponseForbidden('Only club managers can create events.')
    if request.method == 'POST':
        form = EventForm(request.POST, user=request.user)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            if request.user.role == 'admin':
                return redirect('admin_dashboard')
            return redirect('manager_dashboard')
    else:
        form = EventForm(user=request.user)
    return render(request, 'event_form.html', {'form': form})


@login_required
def edit_event(request, pk):
    event = get_object_or_404(Event, id=pk)
    if event.created_by != request.user and request.user.role != 'admin':
        return HttpResponseForbidden('You can only edit your own events.')
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('event_detail', pk=pk)
    else:
        form = EventForm(instance=event, user=request.user)
    return render(request, 'event_form.html', {'form': form, 'edit': True})


@login_required
def delete_event(request, pk):
    event = get_object_or_404(Event, id=pk)
    if event.created_by != request.user and request.user.role != 'admin':
        return HttpResponseForbidden('Access denied.')
    event.delete()
    return redirect('events')


@login_required
def event_detail(request, pk):
    event = get_object_or_404(Event, id=pk)
    is_registered = EventRegistration.objects.filter(event=event, user=request.user).exists()
    participants = EventRegistration.objects.filter(event=event).select_related('user')
    context = {
        'event': event,
        'is_registered': is_registered,
        'is_full': event.is_full(),
        'participants': participants,
    }
    return render(request, 'event_detail.html', context)


@login_required
def register_event(request, pk):
    event = get_object_or_404(Event, id=pk)
    if event.is_full():
        return HttpResponseForbidden('Event is full.')
    EventRegistration.objects.get_or_create(event=event, user=request.user)
    return redirect('event_detail', pk=pk)


@login_required
def cancel_registration(request, pk):
    event = get_object_or_404(Event, id=pk)
    EventRegistration.objects.filter(event=event, user=request.user).delete()
    return redirect('event_detail', pk=pk)
