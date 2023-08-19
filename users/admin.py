from django.contrib import admin
from .models import Profile, Candidate, Worker, Client
admin.site.register(Profile)
admin.site.register(Candidate)
admin.site.register(Worker)
admin.site.register(Client)
