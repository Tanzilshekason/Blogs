from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('create/', views.post_create, name='post_create'),
    path('edit/<int:pk>/', views.post_update, name='post_update'),
    path('delete/<int:pk>/', views.post_delete, name='post_delete'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    # path('notifications/', views.notification_list, name='notification_list'),
    path('post/<int:post_id>/follow/', views.follow_post, name='follow_post'),
    path('post/<int:post_id>/unfollow/', views.unfollow_post, name='unfollow_post'),
    path('notifications/', views.notification_list, name='notifications'),
    path('post/<int:post_id>/rate/', views.rate_post, name='rate_post'),
    path('rate/<int:post_id>/', views.rate_post, name='rate_post'),


    



    # path('followed/', views.followed_posts, name='followed_posts'),

]
