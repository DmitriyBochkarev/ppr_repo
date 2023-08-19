from django.shortcuts import render, get_object_or_404
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
from users.models import Candidate
from django.contrib import messages


def home(request):
    context = {
        'tasks': Task.objects.all()
    }
    return render(request, 'searchwork/home.html', context)


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
    success_url = '/'


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
        print (Task.objects.get(id=self.kwargs.get('pk')).author.username)
        print (self.request.user)
        if Candidate.objects.filter(task=self.kwargs.get('pk'), user=self.request.user):
            messages.warning(self.request, 'Вы уже откликались на данную задачу.')
            return render(self.request, 'searchwork/task_detail.html', {
        'object': Task.objects.get(id=self.kwargs.get('pk'))
    })
        else:
            form.instance.user = self.request.user
            form.instance.task = Task.objects.get(id=self.kwargs.get('pk'))
            messages.success(self.request, 'Ваш отклик успешно доставлен.')
            return super().form_valid(form)

class CandidateListView(ListView):
    model = Candidate
    template_name = 'searchwork/task_candidates.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'candidates'
    paginate_by = 10

    def get_queryset(self):
        candidate = get_object_or_404(Task, id=self.kwargs.get('pk'))
        return Candidate.objects.filter(task=candidate).order_by('-user')