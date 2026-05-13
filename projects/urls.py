from django.urls import path 
from .import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('project/create/', views.create_project, name='create_project'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('project/<int:pk>/task/create/', views.create_task, name='create_task'),
    path('task/<int:pk>/', views.task_detail, name='task_detail'),
    path('task/<int:pk>/update/', views.update_task_status, name='update_task_status'),
    path('notifications/', views.notifications_view, name='notifications'),
]

