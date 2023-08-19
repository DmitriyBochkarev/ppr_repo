from django.urls import path
from .views import (
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    UserTaskListView,
    CandidateCreateView,
    CandidateListView,
    MyTaskListView
)
from . import views

urlpatterns = [
    path('', TaskListView.as_view(), name='tasks-home'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('task/<int:pk>/create_candidate', CandidateCreateView.as_view(), name='candidate-create'),
    path('task/<int:pk>/task_candidates', CandidateListView.as_view(), name='task-candidates'),
    path('task/new/', TaskCreateView.as_view(), name='task-create'),
    path('task/<int:pk>/update/', TaskUpdateView.as_view(), name='task-update'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
    path('about/', views.about, name='searchwork-about'),
    path('user/<str:username>', UserTaskListView.as_view(), name='user-tasks'),
    path('user/<str:username>/tasks', MyTaskListView.as_view(), name='my-tasks'),
]
