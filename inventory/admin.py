# inventory/admin.py
from django.contrib import admin
from .models import Item, Peripheral, History

# Isso "registra" os modelos na interface de admin
admin.site.register(Item)
admin.site.register(Peripheral)
admin.site.register(History)