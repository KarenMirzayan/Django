from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('edit_group_expense/<int:id>/', views.edit_group_expense, name='edit_group_expense'),
    path('delete_group_expense/<int:id>/', views.delete_group_expense, name='delete_group_expense'),
] 