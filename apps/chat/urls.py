
from django.urls import path
from . import views

urlpatterns = [
    path('rooms/' , views.RoomListView.as_view(), name='rooms'),
    path('rooms/<int:pk>/' , views.RoomDetailView.as_view() , name='rooms detail'),
    path('rooms/<int:room_id>/messages/' , views.MessageHistoryView.as_view() , name='message history'),
    path('rooms/dm/' , views.create_dm , name='create-dm'),
    path('rooms/group/' , views.create_group , name='create-group')
]