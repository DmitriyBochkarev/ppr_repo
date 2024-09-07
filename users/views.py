from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, MessageForm
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Worker, Conversation, Message, User, Client
from .filters import WorkerFilter, ClientFilter
from django_filters.views import FilterView

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Ваш аккаунт создан: можно войти на сайт.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Ваш профиль успешно обновлен.')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)


class WorkerListView(ListView):
    model = Worker
    template_name = 'users/workers.html'
    context_object_name = 'workers'
    # ordering = ['-date_posted']
    paginate_by = 10

class WorkerFilteredView(FilterView):
    model = Worker
    filterset_class = WorkerFilter
    template_name = 'users/filter_workers.html'  # Укажите ваш шаблон

    def get_queryset(self):
        queryset = super().get_queryset()
        # Применяем сортировку, если указано
        sort_by = self.request.GET.get('sort_by')
        if sort_by:
            queryset = queryset.order_by(sort_by)
            messages.success(self.request,
                         f'Отсортировано по {sort_by}')

        return queryset


class ClientListView(ListView):
    model = Client
    template_name = 'users/clients.html'
    context_object_name = 'clients'
    # ordering = ['-date_posted']
    paginate_by = 10

class ClientFilteredView(FilterView):
    model = Client
    filterset_class = ClientFilter
    template_name = 'users/filter_clients.html'  # Укажите ваш шаблон

    def get_queryset(self):
        queryset = super().get_queryset()
        # Применяем сортировку, если указано
        sort_by = self.request.GET.get('sort_by')
        if sort_by:
            queryset = queryset.order_by(sort_by)
            messages.success(self.request,
                         f'Отсортировано по {sort_by}')

        return queryset

@login_required
def chat_view(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    if Conversation.objects.filter(user1=other_user, user2=request.user) or Conversation.objects.filter(user2=other_user, user1=request.user):
        if Conversation.objects.filter(user1=other_user, user2=request.user):
            conversation, created = Conversation.objects.get_or_create(
            user2=request.user,
            user1=other_user
            )
            chat_messages = Message.objects.filter(conversation=conversation).order_by('-timestamp')
            if request.method == 'POST':
                form = MessageForm(request.POST)
                if form.is_valid():
                    chat_messages = form.save(commit=False)
                    chat_messages.conversation = conversation
                    chat_messages.sender = request.user
                    chat_messages.save()
                    return redirect('chat', user_id=user_id)
            else:
                form = MessageForm()

            return render(request, 'users/chat.html',
                          {'chat_messages': chat_messages, 'other_user': other_user, 'form': form})

        elif Conversation.objects.filter(user2=other_user, user1=request.user):
            conversation, created = Conversation.objects.get_or_create(
                user1=request.user,
                user2=other_user
            )
            chat_messages = Message.objects.filter(conversation=conversation).order_by('-timestamp')
            if request.method == 'POST':
                form = MessageForm(request.POST)
                if form.is_valid():
                    chat_messages = form.save(commit=False)
                    chat_messages.conversation = conversation
                    chat_messages.sender = request.user
                    chat_messages.save()
                    return redirect('chat', user_id=user_id)
            else:
                form = MessageForm()

            return render(request, 'users/chat.html',
                          {'chat_messages': chat_messages, 'other_user': other_user, 'form': form})



    else:
        conversation, created = Conversation.objects.get_or_create(
            user1=request.user,
            user2=other_user
        )
        chat_messages = Message.objects.filter(conversation=conversation).order_by('-timestamp')

        if request.method == 'POST':
            form = MessageForm(request.POST)
            if form.is_valid():
                chat_messages = form.save(commit=False)
                chat_messages.conversation = conversation
                chat_messages.sender = request.user
                chat_messages.save()
                return redirect('chat', user_id=user_id)
        else:
            form = MessageForm()

        return render(request, 'users/chat.html',
                      {'chat_messages': chat_messages, 'other_user': other_user, 'form': form})

def chats(request):
    instance = request.user
    conversations = Conversation.objects.filter(user1=instance)
    conversations2 = Conversation.objects.filter(user2=instance)
    return render(request, 'users/my_chats.html', {
        'conversations': conversations,
        'conversations2': conversations2
    })

def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'users/user_profile.html',
                          {'user': user})
