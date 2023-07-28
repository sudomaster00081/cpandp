from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create-room/', views.create_room, name='create_room'),
    path('enter-room/', views.enter_room, name='enter_room'),
    path('room/<int:room_id>/', views.room_interface, name='room_interface'),
    path('enter-room/', views.enter_room, name='enter_room'),  # Add this URL pattern
    path('room/<str:room_id>/exit/', views.exit_room, name='exit_room'),  # Add this URL pattern for exiting the room
]
