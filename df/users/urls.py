# users/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register, my_logout

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'), # с этой не работало
    path('logout/', my_logout, name='logout'),  # Используем нашу новую вьюху
]
