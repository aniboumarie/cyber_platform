from django.urls import path
from . import views  # Changed to import the views module directly
from .views import (
    home, signup_view, dashboard_view, add_lesson_view,
    admin_dashboard, trainer_dashboard, trainee_dashboard, unauthorized, RoleBasedLoginView,
    manage_users, create_user,
    # Add new course views here if not using the 'views.' prefix approach
    # network_security_view, ethical_hacking_view, cloud_security_view, incident_response_view
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'), # Added views. prefix for consistency
    path('signup/', views.signup_view, name='signup'), # Added views. prefix
    path('login/', views.RoleBasedLoginView.as_view(), name='login'), # Added views. prefix
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'), # LogoutView is imported directly
    path('dashboard/', views.dashboard_view, name='dashboard'), # Added views. prefix
    path('lessons/add/', views.add_lesson_view, name='add_lesson'), # Added views. prefix
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'), # Added views. prefix
    path('trainer-dashboard/', views.trainer_dashboard, name='trainer_dashboard'), # Added views. prefix
    path('trainee-dashboard/', views.trainee_dashboard, name='trainee_dashboard'), # Added views. prefix
    path('unauthorized/', views.unauthorized, name='unauthorized'), # Added views. prefix
    path('manage-users/', views.manage_users, name='manage_users'), # Added views. prefix
    path('create-user/', views.create_user, name='create_user'), # Added views. prefix

    # Static Course Detail Pages (to be removed)
    # path('courses/network-security/', views.network_security_view, name='course_network_security'),
    # path('courses/ethical-hacking/', views.ethical_hacking_view, name='course_ethical_hacking'),
    # path('courses/cloud-security/', views.cloud_security_view, name='course_cloud_security'),
    # path('courses/incident-response/', views.incident_response_view, name='course_incident_response'),

    path('courses/', views.course_catalog_view, name='course_catalog'),
    path('course/<slug:slug>/', views.course_detail_view, name='course_detail'), # This line is already present and correct
]

