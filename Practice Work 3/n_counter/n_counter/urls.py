from django.contrib import admin
from django.urls import path
from app.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('delete/<int:id>/', delete_consume, name="delete"),
    path('api/nutrient_data/', nutrient_data_by_time, name='nutrient_data'),
    path('set_goals/', set_goals, name='set_goals'),
    path("chart-data/", chart_data, name="chart-data"),
    path("register/", register, name="register"),
    path("add-food/", add_food, name="add-food"),
]

urlpatterns += [
    path("login/", auth_views.LoginView.as_view(template_name="app/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
