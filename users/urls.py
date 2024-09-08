from django.contrib.auth import views as auth_views
from . import views as user_views
from . views import WorkerListView, WorkerFilteredView, ClientFilteredView, ClientListView
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('workers', WorkerListView.as_view(), name='workers'),
path('clients', ClientListView.as_view(), name='clients'),
    path('chat/<int:user_id>/', user_views.chat_view, name='chat'),
path('chats', user_views.chats, name='chats'),
path('<int:user_id>/', user_views.user_profile, name='user-profile'),
# path('<str:username>/chats', ChatListView.as_view(), name='my-chats'),
path('filter_workers', WorkerFilteredView.as_view(), name='filter-workers'),
path('filter_clients', ClientFilteredView.as_view(), name='filter-clients'),
path('feedback/', user_views.feedback_view, name='feedback'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

