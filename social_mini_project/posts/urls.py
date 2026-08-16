from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.xxxas_view(), name='post_list'),
    path('create/', views.xxx.as_view(), name='post_create'),
    path('<int:pk>/', views.xxx.as_view(), name='post_detail'),
    path('<int:pk>/edit/', views.xxx.as_view(), name='post_edit'),
    path('<int:pk>/delete/', views.xxx.as_view(), name='post_delete'),
]
