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
    TaskFilteredView,
TaskClientListView,
TaskClientFilteredView,
TaskDetailClientView,
UserTaskClientListView,
ClientProfileView
)
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('instruction', views.instruction, name='instruction'),
    path('news', views.news, name='news'),
    path('task', TaskListView.as_view(), name='tasks-home'),
    path('task_client', TaskClientListView.as_view(), name='tasks-home-client'),
    path('worker', views.worker, name='worker'),
    path('client', views.client, name='client'),
    # path('filter_form', views.filter_view, name='filter-form'),
    path('filter_home', TaskFilteredView.as_view(), name='filter-home'),
    path('filter_home_client', TaskClientFilteredView.as_view(), name='filter-home-client'),
    path('task/<int:pk>/comment_form', views.comment, name='comment-form'),
    path('task/<int:pk>/comment_form_client', views.comment_client, name='comment-form-client'),
    path('task/<int:pk>/task_detail', TaskDetailView.as_view(), name='task-detail'),
    path('task/<int:pk>/task_detail_client', TaskDetailClientView.as_view(), name='task-detail-client'),
    path('task/<int:pk>/create_candidate', CandidateCreateView.as_view(), name='candidate-create'),
    path('task/<int:pk>/task_candidates', CandidateListView.as_view(), name='task-candidates'),
    path('task/new/', TaskCreateView.as_view(), name='task-create'),
    path('task/<int:pk>/update/', TaskUpdateView.as_view(), name='task-update'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
    path('about/', views.about, name='searchwork-about'),
    path('user/<str:username>', UserTaskListView.as_view(), name='user-tasks'),
    path('user/<str:username>/user_tasks_client', UserTaskClientListView.as_view(), name='user-tasks-client'),
    path('user/<str:username>/tasks', MyTaskListView.as_view(), name='my-tasks'),
    path('user/<str:username>/worker_create', CreateWorkerView.as_view(), name='worker-create'),
    path('user/<str:username>/client_create', CreateClientView.as_view(), name='client-create'),
    path('user/<str:username>/my_offers', OfferListView.as_view(), name='my-offers'),
    path('worker/<int:pk>', WorkerProfileView.as_view(), name='worker-profile'),
    path('client/<int:pk>', ClientProfileView.as_view(), name='client-profile'),
    path('worker/<int:pk>/worker_comment_form', views.worker_comment_form, name='worker-comment-form'),
    path('client/<int:pk>/client_comment_form', views.client_comment_form, name='client-comment-form'),
    path('task/<int:pk>/task_candidates/<int:pk1>/worker_to_task/', WorkerToTaskView.as_view(), name='worker-to-task'),
]
