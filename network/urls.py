from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_post/', views.add_post, name='add_post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('users/', views.users_list, name='users'),
    path('send_friend_request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('accept_friend_request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('reject_friend_request/<int:request_id>/', views.reject_friend_request, name='reject_friend_request'),
    path('friend_requests/', views.friend_requests, name='friend_requests'),
    path('send_message/<int:user_id>/', views.send_message, name='send_message'),
    path('messages/<int:user_id>/', views.messages, name='messages'),
    path('message_list/', views.message_list, name='message_list'),
    path('profile/', views.profile, name='profile'),  
    path('splash/', views.splash, name='splash'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
