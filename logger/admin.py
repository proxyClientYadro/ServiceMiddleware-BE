from django.contrib import admin

from logger.models import LogModel


@admin.register(LogModel)
class LogModelAdmin(admin.ModelAdmin):
    ordering = ('id', 'created_at', 'proxy_method',)
