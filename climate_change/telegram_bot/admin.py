from django.contrib import admin
from .models import *

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ['modify_user']
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'modify_user', None) is None:
            obj.modify_user = request.user
        obj.save()

admin.site.register(Knowledge, PostAdmin)
admin.site.register(Policy, PostAdmin)
admin.site.register(TelegramChat)