from django.contrib import admin
from .models import Quantity

@admin.register(Quantity)
class QuantityAdmin(admin.ModelAdmin):
    list_display = ['date', 'time', 'quantity']
