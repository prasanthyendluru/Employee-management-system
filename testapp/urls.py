from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Authentication
    path('signup/', views.signup, name='signup'),
    path('manager/login/', views.manager_login, name='manager_login'),
    path('employee/login/', views.employee_login, name='employee_login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),

    # Dashboards
    path('manager/dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('employee/dashboard/', views.employee_dashboard, name='employee_dashboard'),

    # Task Management
    path('task/assign/', views.assign_task, name='assign_task'),
    path('task/<int:task_id>/update-status/', views.update_task_status, name='update_task_status'),
]