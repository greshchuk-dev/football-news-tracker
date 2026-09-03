from django.contrib import admin
from .models import NewsArticle, Team
from django_apscheduler.models import DjangoJob, DjangoJobExecution

admin.site.register(DjangoJob)
admin.site.register(DjangoJobExecution)

@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_at', 'source_name', 'team')
    search_fields = ('title', 'author', 'source_name')
    list_filter = ('published_at', 'source_name', 'team')

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'search_query')
