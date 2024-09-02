from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Task, Comment
from django.contrib.auth.models import User
from users.models import Candidate, Worker, Client, Profile
from django.contrib import messages
# from . forms import FilterForm
from .filters import TaskFilter
from django_filters.views import FilterView
from .forms import CommentForm
from users.forms import WorkerCommentForm, ClientCommentForm


class TaskListView(ListView):
    model = Task
    template_name = 'searchwork/home.html'
    context_object_name = 'tasks'
    ordering = ['-date_posted']
    paginate_by = 10


class TaskClientListView(ListView):
    model = Task
    template_name = 'searchwork/home_client.html'
    context_object_name = 'tasks'
    ordering = ['-date_posted']
    paginate_by = 10


class TaskDetailView(DetailView):
    model = Task
    # def get_queryset(self, pk):
    #     task = Task.objects.get(pk=pk)
    #     comments = task.comments.all()
    #     return render(self.request, 'searchwork/task_detail.html', {'task': task, 'comments': comments})
class TaskDetailClientView(DetailView):
    model = Task
    template_name = 'searchwork/task_detail_client.html'


def comment(request, pk):
    task = Task.objects.get(pk=pk)
    comments = task.comments.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.author = request.user
            comment.save()
            return redirect('comment-form', pk=task.pk)
    else:
        form = CommentForm()

    return render(request, 'searchwork/comment_form.html', {'task': task, 'comments': comments, 'form': form})


def comment_client(request, pk):
    task = Task.objects.get(pk=pk)
    comments = task.comments.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.author = request.user
            comment.save()
            return redirect('comment-form-client', pk=task.pk)
    else:
        form = CommentForm()

    return render(request, 'searchwork/comment_form_client.html', {'task': task, 'comments': comments, 'form': form})

def worker_comment_form(request, pk):
    worker = Worker.objects.get(pk=pk)
    worker_comments = worker.worker_comments.all()

    if request.method == 'POST':
        form = WorkerCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.worker = worker
            comment.author = request.user
            comment.save()
            return redirect('worker-comment-form', pk=worker.pk)
    else:
        form = WorkerCommentForm()

    return render(request, 'users/worker_comment_form.html', {'worker': worker, 'worker_comments': worker_comments, 'form': form})

def client_comment_form(request, pk):
    client = Client.objects.get(pk=pk)
    client_comments = client.client_comments.all()

    if request.method == 'POST':
        form = ClientCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.client = client
            comment.author = request.user
            comment.save()
            return redirect('client-comment-form', pk=client.pk)
    else:
        form = ClientCommentForm()

    return render(request, 'users/client_comment_form.html', {'client': client, 'client_comments': client_comments, 'form': form})


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'content', 'status', 'budget', 'type', 'category']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    fields = ['title', 'content', 'status', 'budget', 'type', 'category']

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

class UserTaskClientListView(ListView):
    model = Task
    template_name = 'searchwork/user_tasks_client.html'  # <app>/<model>_<viewtype>.html
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
    fields = ['offer']

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
    fields = ['about']

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

        return redirect('my-tasks', username=request.user.username)
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
        worker = self.request.user.worker
        return Candidate.objects.filter(worker=worker).order_by('-task')


class WorkerProfileView(DetailView):
    """template worker_detail"""
    model = Worker

class ClientProfileView(DetailView):
    """template client_detail"""
    model = Client

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


# def filter_view(request):
#     # функция для представления формы фильтров
#     if request.method == 'POST':
#         form = FilterForm(request.POST)
#         if form.is_valid():
#
#             category = form.cleaned_data.get('category')
#             type = form.cleaned_data.get('type')
#             budget_to = form.cleaned_data.get('budget_to')
#             budget_from = form.cleaned_data.get('budget_from')
#             status = form.cleaned_data.get('status')
#             ordering_budget = form.cleaned_data.get('ordering_budget')
#             ordering_date = form.cleaned_data.get('ordering_date')
#             if category == 'Любой' and type != 'Любой' and status != 'Любой':
#                 messages.success(request,
#                                  f'Отфильтрованы задачи с категорией: "{category}", с типом: "{type}", со статусом: "{status}", c бюджетом от: {budget_from} до: {budget_to} руб.')
#                 if ordering_budget == 'Нет' and ordering_date == 'Сначала новые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(type=type, status=status, budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('-date_posted')})
#                 elif ordering_budget == 'Нет' and ordering_date == 'Сначала старые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(type=type, status=status, budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('date_posted')})
#
#                 elif ordering_budget == 'По возрастанию' and ordering_date == 'Нет':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(type=type, status=status, budget__lt=budget_to, budget__gt=budget_from).order_by('budget')})
#                 elif ordering_budget == 'По убыванию' and ordering_date == 'Нет':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(type=type, status=status, budget__lt=budget_to, budget__gt=budget_from).order_by('-budget')})
#                 elif ordering_budget == 'По возрастанию' and ordering_date == 'Сначала новые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(type=type, status=status, budget__lt=budget_to, budget__gt=budget_from).order_by('budget', '-date_posted')})
#                 elif ordering_budget == 'По возрастанию' and ordering_date == 'Сначала старые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(type=type, status=status, budget__lt=budget_to, budget__gt=budget_from).order_by('budget', 'date_posted')})
#                 elif ordering_budget == 'По убыванию' and ordering_date == 'Сначала новые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(type=type, status=status, budget__lt=budget_to, budget__gt=budget_from).order_by('-budget', '-date_posted')})
#                 elif ordering_budget == 'По убыванию' and ordering_date == 'Сначала старые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(type=type, status=status, budget__lt=budget_to, budget__gt=budget_from).order_by('-budget', 'date_posted')})
#                 else:
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(type=type, status=status, budget__lt=budget_to,
#                                                                 budget__gt=budget_from)})
#
#             elif type == 'Любой' and category != 'Любой' and status != 'Любой':
#                 messages.success(request, f'Отфильтрованы задачи с категорией: "{category}", с типом: "{type}", со статусом: "{status}", c бюджетом от: {budget_from} до: {budget_to} руб.')
#                 if ordering_budget == 'Нет' and ordering_date == 'Сначала новые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(category=category, status=status, budget__lt=budget_to, budget__gt=budget_from).order_by('-date_posted')})
#                 elif ordering_budget == 'Нет' and ordering_date == 'Сначала старые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(category=category, status=status, budget__lt=budget_to, budget__gt=budget_from).order_by('date_posted')})
#
#                 elif ordering_budget == 'По возрастанию' and ordering_date == 'Нет':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(category=category, status=status, budget__lt=budget_to, budget__gt=budget_from).order_by('budget')})
#                 elif ordering_budget == 'По убыванию' and ordering_date == 'Нет':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(category=category, status=status, budget__lt=budget_to, budget__gt=budget_from).order_by('-budget')})
#                 elif ordering_budget == 'По возрастанию' and ordering_date == 'Сначала новые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(category=category, status=status, budget__lt=budget_to, budget__gt=budget_from).order_by('budget', '-date_posted')})
#                 elif ordering_budget == 'По возрастанию' and ordering_date == 'Сначала старые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(category=category, status=status, budget__lt=budget_to, budget__gt=budget_from).order_by('budget', 'date_posted')})
#                 elif ordering_budget == 'По убыванию' and ordering_date == 'Сначала новые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(category=category, status=status, budget__lt=budget_to, budget__gt=budget_from).order_by('-budget', '-date_posted')})
#                 elif ordering_budget == 'По убыванию' and ordering_date == 'Сначала старые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(category=category, status=status, budget__lt=budget_to, budget__gt=budget_from).order_by('-budget', 'date_posted')})
#                 else:
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(category=category, status=status, budget__lt=budget_to, budget__gt=budget_from)})
#             elif status == 'Любой' and category != 'Любой' and type != 'Любой':
#                 messages.success(request, f'Отфильтрованы задачи с категорией: "{category}", с типом: "{type}", со статусом: "{status}", c бюджетом от: {budget_from} до: {budget_to} руб.')
#                 if ordering_budget == 'Нет' and ordering_date == 'Сначала новые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(category=category, type=type, budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('-date_posted')})
#                 elif ordering_budget == 'Нет' and ordering_date == 'Сначала старые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(category=category, type=type, budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('date_posted')})
#
#                 elif ordering_budget == 'По возрастанию' and ordering_date == 'Нет':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(category=category, type=type, budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('budget')})
#                 elif ordering_budget == 'По убыванию' and ordering_date == 'Нет':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(category=category, type=type, budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('-budget')})
#                 elif ordering_budget == 'По возрастанию' and ordering_date == 'Сначала новые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(category=category, type=type, budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('budget',
#                                                                                                  '-date_posted')})
#                 elif ordering_budget == 'По возрастанию' and ordering_date == 'Сначала старые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(category=category, type=type, budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('budget',
#                                                                                                  'date_posted')})
#                 elif ordering_budget == 'По убыванию' and ordering_date == 'Сначала новые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(category=category, type=type, budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('-budget',
#                                                                                                  '-date_posted')})
#                 elif ordering_budget == 'По убыванию' and ordering_date == 'Сначала старые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(category=category, type=type, budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('-budget',
#                                                                                                  'date_posted')})
#                 else:
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(category=category, type=type, budget__lt=budget_to,
#                                                                 budget__gt=budget_from)})
#
#             elif type == 'Любой' and category == 'Любой' and status == 'Любой':
#                 messages.success(request, f'Отфильтрованы задачи с категорией: "{category}", с типом: "{type}", со статусом: "{status}", c бюджетом от: {budget_from} до: {budget_to} руб.')
#                 if ordering_budget == 'Нет' and ordering_date == 'Сначала новые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('-date_posted')})
#                 elif ordering_budget == 'Нет' and ordering_date == 'Сначала старые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('date_posted')})
#
#                 elif ordering_budget == 'По возрастанию' and ordering_date == 'Нет':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('budget')})
#                 elif ordering_budget == 'По убыванию' and ordering_date == 'Нет':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('-budget')})
#                 elif ordering_budget == 'По возрастанию' and ordering_date == 'Сначала новые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('budget',
#                                                                                                  '-date_posted')})
#                 elif ordering_budget == 'По возрастанию' and ordering_date == 'Сначала старые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('budget',
#                                                                                                  'date_posted')})
#                 elif ordering_budget == 'По убыванию' and ordering_date == 'Сначала новые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('-budget',
#                                                                                                  '-date_posted')})
#                 elif ordering_budget == 'По убыванию' and ordering_date == 'Сначала старые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('-budget',
#                                                                                                  'date_posted')})
#                 else:
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(budget__lt=budget_to,
#                                                                 budget__gt=budget_from)})
#             elif type != 'Любой' and category == 'Любой' and status == 'Любой':
#                 messages.success(request, f'Отфильтрованы задачи с категорией: "{category}", с типом: "{type}", со статусом: "{status}", c бюджетом от: {budget_from} до: {budget_to} руб.')
#                 if ordering_budget == 'Нет' and ordering_date == 'Сначала новые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(type=type, budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('-date_posted')})
#                 elif ordering_budget == 'Нет' and ordering_date == 'Сначала старые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(type=type, budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('date_posted')})
#
#                 elif ordering_budget == 'По возрастанию' and ordering_date == 'Нет':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(type=type, budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('budget')})
#                 elif ordering_budget == 'По убыванию' and ordering_date == 'Нет':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(type=type, budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('-budget')})
#                 elif ordering_budget == 'По возрастанию' and ordering_date == 'Сначала новые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(type=type, budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('budget',
#                                                                                                  '-date_posted')})
#                 elif ordering_budget == 'По возрастанию' and ordering_date == 'Сначала старые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(type=type, budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('budget',
#                                                                                                  'date_posted')})
#                 elif ordering_budget == 'По убыванию' and ordering_date == 'Сначала новые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(type=type, budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('-budget',
#                                                                                                  '-date_posted')})
#                 elif ordering_budget == 'По убыванию' and ordering_date == 'Сначала старые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(type=type, budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('-budget',
#                                                                                                  'date_posted')})
#                 else:
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(type=type, budget__lt=budget_to,
#                                                                 budget__gt=budget_from)})
#             elif type == 'Любой' and category != 'Любой' and status == 'Любой':
#                 messages.success(request, f'Отфильтрованы задачи с категорией: "{category}", с типом: "{type}", со статусом: "{status}", c бюджетом от: {budget_from} до: {budget_to} руб.')
#                 if ordering_budget == 'Нет' and ordering_date == 'Сначала новые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(category=category, budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('-date_posted')})
#                 elif ordering_budget == 'Нет' and ordering_date == 'Сначала старые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(category=category, budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('date_posted')})
#
#                 elif ordering_budget == 'По возрастанию' and ordering_date == 'Нет':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(category=category, budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('budget')})
#                 elif ordering_budget == 'По убыванию' and ordering_date == 'Нет':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(category=category, budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('-budget')})
#                 elif ordering_budget == 'По возрастанию' and ordering_date == 'Сначала новые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(category=category, budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('budget',
#                                                                                                  '-date_posted')})
#                 elif ordering_budget == 'По возрастанию' and ordering_date == 'Сначала старые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(category=category, budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('budget',
#                                                                                                  'date_posted')})
#                 elif ordering_budget == 'По убыванию' and ordering_date == 'Сначала новые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(category=category, budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('-budget',
#                                                                                                  '-date_posted')})
#                 elif ordering_budget == 'По убыванию' and ordering_date == 'Сначала старые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(category=category, budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('-budget',
#                                                                                                  'date_posted')})
#                 else:
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(category=category, budget__lt=budget_to,
#                                                                 budget__gt=budget_from)})
#
#             elif type == 'Любой' and category == 'Любой' and status != 'Любой':
#                 messages.success(request, f'Отфильтрованы задачи с категорией: "{category}", с типом: "{type}", со статусом: "{status}", c бюджетом от: {budget_from} до: {budget_to} руб.')
#                 if ordering_budget == 'Нет' and ordering_date == 'Сначала новые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(status=status, budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('-date_posted')})
#                 elif ordering_budget == 'Нет' and ordering_date == 'Сначала старые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(status=status, budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('date_posted')})
#
#                 elif ordering_budget == 'По возрастанию' and ordering_date == 'Нет':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(status=status, budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('budget')})
#                 elif ordering_budget == 'По убыванию' and ordering_date == 'Нет':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(status=status, budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('-budget')})
#                 elif ordering_budget == 'По возрастанию' and ordering_date == 'Сначала новые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(status=status, budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('budget',
#                                                                                                  '-date_posted')})
#                 elif ordering_budget == 'По возрастанию' and ordering_date == 'Сначала старые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(status=status, budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('budget',
#                                                                                                  'date_posted')})
#                 elif ordering_budget == 'По убыванию' and ordering_date == 'Сначала новые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(status=status, budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('-budget',
#                                                                                                  '-date_posted')})
#                 elif ordering_budget == 'По убыванию' and ordering_date == 'Сначала старые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(status=status, budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('-budget',
#                                                                                                  'date_posted')})
#                 else:
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(status=status, budget__lt=budget_to,
#                                                                 budget__gt=budget_from)})
#             else:
#                 messages.success(request, f'Отфильтрованы задачи с категорией: "{category}", с типом: "{type}", со статусом: "{status}", c бюджетом от: {budget_from} до: {budget_to} руб.')
#                 if ordering_budget == 'Нет' and ordering_date == 'Сначала новые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(category=category, type=type, status=status, budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('-date_posted')})
#                 elif ordering_budget == 'Нет' and ordering_date == 'Сначала старые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(category=category, type=type, status=status, budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('date_posted')})
#
#                 elif ordering_budget == 'По возрастанию' and ordering_date == 'Нет':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(category=category, type=type, status=status, budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('budget')})
#                 elif ordering_budget == 'По убыванию' and ordering_date == 'Нет':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(category=category, type=type, status=status, budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('-budget')})
#                 elif ordering_budget == 'По возрастанию' and ordering_date == 'Сначала новые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(category=category, type=type, status=status, budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('budget',
#                                                                                                  '-date_posted')})
#                 elif ordering_budget == 'По возрастанию' and ordering_date == 'Сначала старые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(category=category, type=type, status=status, budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('budget',
#                                                                                                  'date_posted')})
#                 elif ordering_budget == 'По убыванию' and ordering_date == 'Сначала новые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(category=category, type=type, status=status, budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('-budget',
#                                                                                                  '-date_posted')})
#                 elif ordering_budget == 'По убыванию' and ordering_date == 'Сначала старые':
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(category=category, type=type, status=status, budget__lt=budget_to,
#                                                                 budget__gt=budget_from).order_by('-budget',
#                                                                                                  'date_posted')})
#                 else:
#                     return render(request, 'searchwork/home.html',
#                                   {'tasks': Task.objects.filter(category=category, type=type, status=status, budget__lt=budget_to,
#                                                                 budget__gt=budget_from)})
#
#     else:
#         form = FilterForm()
#
#     return render(request, 'searchwork/filter_form.html', {'form': form})


class TaskFilteredView(FilterView):
    model = Task
    filterset_class = TaskFilter
    template_name = 'searchwork/filter_home.html'  # Укажите ваш шаблон

    def get_queryset(self):
        queryset = super().get_queryset()
        # Применяем сортировку, если указано
        sort_by = self.request.GET.get('sort_by')
        if sort_by:
            queryset = queryset.order_by(sort_by)
            messages.success(self.request,
                         f'Отсортировано по {sort_by}')

        return queryset

class TaskClientFilteredView(FilterView):
    model = Task
    filterset_class = TaskFilter
    template_name = 'searchwork/filter_home_client.html'  # Укажите ваш шаблон

    def get_queryset(self):
        queryset = super().get_queryset()
        # Применяем сортировку, если указано
        sort_by = self.request.GET.get('sort_by')
        if sort_by:
            queryset = queryset.order_by(sort_by)
            messages.success(self.request,
                         f'Отсортировано по {sort_by}')

        return queryset