from django.contrib import admin
from .models import Tag, Dispatch, Client, Message, MobileOperatorCode

admin.site.register(Tag)
admin.site.register(Dispatch)
admin.site.register(Client)
admin.site.register(Message)
admin.site.register(MobileOperatorCode)
