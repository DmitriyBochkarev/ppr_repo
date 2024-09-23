from django.contrib import admin
from .models import Profile, Candidate, Worker, Client, WorkerComment, Conversation, Message, ClientComment, Feedback
admin.site.register(Profile)
admin.site.register(Candidate)
admin.site.register(Worker)
admin.site.register(Client)
admin.site.register(WorkerComment)
admin.site.register(Conversation)
admin.site.register(Message)
admin.site.register(ClientComment)
admin.site.register(Feedback)
