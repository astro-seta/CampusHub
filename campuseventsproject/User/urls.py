from django.urls import path
from .views import accountsView
urlpatterns=[
   path('',accountsView.as_view(),name='account') 
]