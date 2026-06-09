from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class accountsView(TemplateView):
    template_name='accounts.html'