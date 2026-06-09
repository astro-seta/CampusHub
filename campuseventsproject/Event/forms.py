from django import forms
from .models import Event
from Club.models import Club

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'club', 'max_participants']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'title': forms.TextInput(attrs={'placeholder': 'Event title'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user and user.role == 'club_manager':
            self.fields['club'].queryset = Club.objects.filter(owner=user, is_approved=True)
        elif user and user.role == 'admin':
            self.fields['club'].queryset = Club.objects.filter(is_approved=True)