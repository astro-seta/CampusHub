from django.urls import path
from .views import eventsView, create_event, edit_event, delete_event, event_detail, register_event, cancel_registration

urlpatterns = [
    path('', eventsView.as_view(), name='events'),
    path('club/<int:club_id>/', eventsView.as_view(), name='ClubEvents'),
    path('create/', create_event, name='create_event'),
    path('<int:pk>/', event_detail, name='event_detail'),
    path('<int:pk>/edit/', edit_event, name='edit_event'),
    path('<int:pk>/delete/', delete_event, name='delete_event'),
    path('<int:pk>/register/', register_event, name='register_event'),
    path('<int:pk>/cancel/', cancel_registration, name='cancel_registration'),
]