from django.urls import path
from .views import (
    home, signup_view, dashboard_view, add_lesson_view,
    admin_dashboard, trainer_dashboard, trainee_dashboard, unauthorized, RoleBasedLoginView,
    manage_users, create_user
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup_view, name='signup'),
    path('login/', RoleBasedLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('lessons/add/', add_lesson_view, name='add_lesson'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('trainer-dashboard/', trainer_dashboard, name='trainer_dashboard'),
    path('trainee-dashboard/', trainee_dashboard, name='trainee_dashboard'),
    path('unauthorized/', unauthorized, name='unauthorized'),
    path('manage-users/', manage_users, name='manage_users'),
    path('create-user/', create_user, name='create_user'),
]

