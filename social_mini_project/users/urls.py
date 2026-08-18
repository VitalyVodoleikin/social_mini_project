from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'users'

urlpatterns = [
    # Вывод всех пользователей
    path('', views.ProfileListView.as_view(), name='profiles'),

    # Регистрация, авторизация и выход
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='users/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),

    # Профили
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    path('profile/<str:username>/', views.ProfileView.as_view(), name='profile'),
]
