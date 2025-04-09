from django.contrib import admin
from .models import *


@admin.register(Message)
class Message(admin.ModelAdmin):
    list_display = ('date','time','message')
