from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_update_view, name='profile_update'),
    
    # path for admin page
    #path('admin/', views.admin, name='admin'),
]