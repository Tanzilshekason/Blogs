from django.urls import path
from . import views

urlpatterns = [
    path('blog', views.blog_list, name='blog_list'),
    path('create/', views.blog_create, name='blog_create'),
    path('<int:pk>/edit/', views.blog_update, name='blog_update'),
    path('<int:pk>/delete/', views.blog_delete, name='blog_delete'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),

    #comments paths
    #path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    #path('<int:pk>/comment/', views.add_comment, name='add_comment'),
]
