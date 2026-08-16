from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Регистрация, авторизация и выход
    path('register/', views.xxx.as_view(), name='register'),
    path('login/', views.xxx.as_view(), name='login'),
    path('logout/', views.xxx.as_view(), name='logout'),

    # Профили
    path('profile/<str:username>/', views.xxx.as_view(), name='profile'),
    path('profile/edit/', views.xxx.as_view(), name='profile_edit'),
]
