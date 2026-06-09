from django.shortcuts import render
from django.views.generic import TemplateView
from Club.models import Club
from Event.models import Event
from django.utils import timezone
from django.db.models import Count 

class homeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['upcoming_events'] = Event.objects.filter(
            date__gte=timezone.now()
        ).order_by('date')[:5]
        context['popular_clubs'] = Club.objects.filter(is_approved=True).annotate(member_count=Count('members')).order_by('-member_count')[:6]
        return context