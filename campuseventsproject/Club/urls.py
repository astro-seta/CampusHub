from django.urls import path
from .views import clubsView, create_club, edit_club, delete_club, club_detail, join_club, leave_club, approve_club, reject_club, club_members

urlpatterns = [
    path('', clubsView.as_view(), name='clubs'),
    path('<int:pk>/', club_detail, name='club_detail'),
    path('create/', create_club, name='create_club'),
    path('<int:pk>/edit/', edit_club, name='edit_club'),
    path('<int:pk>/delete/', delete_club, name='delete_club'),
    path('<int:pk>/join/', join_club, name='join_club'),
    path('<int:pk>/leave/', leave_club, name='leave_club'),
    path('<int:pk>/approve/', approve_club, name='approve_club'),
    path('<int:pk>/reject/', reject_club, name='reject_club'),
    path('<int:pk>/members/', club_members, name='club_members'),
]