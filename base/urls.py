from django.urls import path
from base import views

urlpatterns = [
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    path('', views.home, name='home'),
    path('room/<str:pk>', views.room, name='room'),
    path('add_room/', views.createRoom, name='create_room' ),
    path('delete_room/<str:room_id>', views.deleteRoom, name="delete_room"),
    path('edit_rooms/<str:room_id>', views.editRoom, name="edit_room"),
    path('delete_comment/<str:comment_id>', views.deleteComment, name="delete_comment")
]