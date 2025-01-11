# users/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register, my_logout
from .views import CustomLoginView  # Импортируйте кастомный класс

urlpatterns = [
    path('register/', register, name='register'),
    #path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', my_logout, name='logout'),  # Используем нашу новую вьюху
]


# from django.contrib import admin
# from django.urls import path, include
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('users/', include('users.urls')),  # Подключаем маршруты приложения users
#     path('', include('catalog.urls')),  # Подключаем маршруты каталога
# ]
