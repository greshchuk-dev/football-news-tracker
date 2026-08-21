from django.shortcuts import render
from .models import NewsArticle

def article_list(request):
    articles = NewsArticle.objects.order_by('-published_at')
    return render(request, 'news/article_list.html', {'articles': articles})