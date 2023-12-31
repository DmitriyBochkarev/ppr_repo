from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Task
from django.contrib.auth.models import User
from users.models import Candidate, Worker, Client, Profile
from django.contrib import messages
# from .forms import CreateWorkerView



class TaskListView(ListView):
    model = Task
    template_name = 'searchwork/home.html'
    context_object_name = 'tasks'
    ordering = ['-date_posted']
    paginate_by = 10


class TaskDetailView(DetailView):
    model = Task


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'content', 'status']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    fields = ['title', 'content', 'status']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        task = self.get_object()
        if self.request.user == task.author:
            return True
        return False


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    success_url = '/task/new/'

    def test_func(self):
        task = self.get_object()
        if self.request.user == task.author:
            return True
        return False


def about(request):
    return render(request, 'searchwork/about.html', {'title': 'О клубе PPR.net'})


class UserTaskListView(ListView):
    model = Task
    template_name = 'searchwork/user_tasks.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'tasks'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Task.objects.filter(author=user).order_by('-date_posted')


class MyTaskListView(ListView):
    model = Task
    template_name = 'searchwork/my_tasks.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'tasks'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Task.objects.filter(author=user).order_by('-date_posted')


class CandidateCreateView(CreateView):
    model = Candidate
    fields = []

    def form_valid(self, form):
        if Candidate.objects.filter(task=self.kwargs.get('pk'), worker=self.request.user.worker):
            messages.warning(self.request, 'Вы уже откликались на данную задачу.')
            return render(self.request, 'searchwork/task_detail.html', {
                'object': Task.objects.get(id=self.kwargs.get('pk'))
            })
        else:
            form.instance.worker = self.request.user.worker
            form.instance.task = Task.objects.get(id=self.kwargs.get('pk'))
            messages.success(self.request, 'Ваш отклик успешно доставлен.')
            return super().form_valid(form)


class CandidateListView(ListView):
    model = Candidate
    template_name = 'searchwork/task_candidates.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'candidates'
    paginate_by = 10

    def get_queryset(self):
        task = get_object_or_404(Task, id=self.kwargs.get('pk'))
        return Candidate.objects.filter(task=task).order_by('-worker')


class CreateWorkerView(CreateView):
    model = Worker
    fields = ['experience']

    def form_valid(self, form):

        form.instance.user = self.request.user
        messages.success(self.request, 'Вы зарегистрированы как исполнитель.')
        return super().form_valid(form)


class CreateClientView(CreateView):
    model = Client
    fields = []

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Вы зарегистрированы как заказчик.')
        return super().form_valid(form)

def worker(request):
    if Worker.objects.filter(user=request.user):
        return redirect('tasks-home')
    else:
        return render(request, 'users/worker_create.html')


def client(request):
    if Client.objects.filter(user=request.user):

        return redirect('my-tasks', username= request.user.username)
    else:
        return render(request, 'users/client_create.html')

def home(request):
    return render(request, 'searchwork/about.html')


class OfferListView(ListView):
    model = Candidate
    template_name = 'searchwork/my_offers.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'offers'
    paginate_by = 10

    def get_queryset(self):
        worker=self.request.user.worker
        return Candidate.objects.filter(worker=worker).order_by('-task')


class WorkerProfileView(DetailView):
    model = Worker


class WorkerToTaskView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        user = User.objects.get(id=self.kwargs.get('pk1'))

        form.instance.worker = user
        form.instance.status = 'В процессе'
        messages.success(self.request, 'Исполнитель назначен. Статус задачи изменен на "В процессе".')
        return super().form_valid(form)

    def test_func(self):
        task = self.get_object()
        if self.request.user == task.author:
            return True
        return False