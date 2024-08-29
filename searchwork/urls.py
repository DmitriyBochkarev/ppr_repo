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
    MyTaskListView,
    CreateWorkerView,
    CreateClientView,
    OfferListView,
    WorkerProfileView,
    WorkerToTaskView,
    TaskFilteredView
)
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('task', TaskListView.as_view(), name='tasks-home'),
    path('worker', views.worker, name='worker'),
    path('client', views.client, name='client'),
    # path('filter_form', views.filter_view, name='filter-form'),
    path('filter_home', TaskFilteredView.as_view(), name='filter-home'),

    path('task/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('task/<int:pk>/create_candidate', CandidateCreateView.as_view(), name='candidate-create'),
    path('task/<int:pk>/task_candidates', CandidateListView.as_view(), name='task-candidates'),
    path('task/new/', TaskCreateView.as_view(), name='task-create'),
    path('task/<int:pk>/update/', TaskUpdateView.as_view(), name='task-update'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
    path('about/', views.about, name='searchwork-about'),
    path('user/<str:username>', UserTaskListView.as_view(), name='user-tasks'),
    path('user/<str:username>/tasks', MyTaskListView.as_view(), name='my-tasks'),
    path('user/<str:username>/worker_create', CreateWorkerView.as_view(), name='worker-create'),
    path('user/<str:username>/client_create', CreateClientView.as_view(), name='client-create'),
    path('user/<str:username>/my_offers', OfferListView.as_view(), name='my-offers'),
    path('worker/<int:pk>', WorkerProfileView.as_view(), name='worker-profile'),

    path('task/<int:pk>/task_candidates/<int:pk1>/worker_to_task/', WorkerToTaskView.as_view(), name='worker-to-task'),
]
