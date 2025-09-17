from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('add/', views.add_todo, name='add'),
    path('edit/<int:pk>/', views.edit_todo, name='edit'),
    path('delete/<int:pk>/', views.delete_todo, name='delete'),
    path('complete/<int:pk>/', views.complete_todo, name='complete'),
]
