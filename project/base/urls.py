from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('create-room/', views.roomCrateion, name='create-room'),
    path('topics/', views.topics, name='topics'),
    path('login/', views.login, name='login'),
    path('register/', views.registerUser, name='register'),
    path('logout/', views.logout, name='logout'),
    path('room/<str:pk>/inside/room', views.room, name='room'),
    path('edit/room/<str:pk>/Edit', views.editRoom, name='edit-room'),
    path('delete/message/<str:pk>/Delete', views.deleteMessage, name='delete-message'),
    path('delete/room-message/<str:pk>/Delete', views.deleteRoomMessage, name='delete-room-message'),
    path('delete/room/<str:pk>/Delete', views.deleteRoom, name='delete-room'),
    path('profile/<str:pk>/Activities', views.profile, name='profile'),
    path('edit-profile/<str:pk>/My-Profile', views.editProfile, name='edit-profile'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)