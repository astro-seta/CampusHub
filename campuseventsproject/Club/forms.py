from django import forms
from .models import Club

class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['name', 'description', 'logo']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Club name'}),
            'description': forms.Textarea(attrs={'placeholder': 'Club description'}),
        }

class ClubFilterForm(forms.Form):
    name = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Search by name'}))