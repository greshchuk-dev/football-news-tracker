from django.contrib import admin
from .models import NewsArticle, Team

@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_at', 'source_name')
    search_fields = ('title', 'author', 'source_name')
    list_filter = ('published_at', 'source_name')

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'search_query')
