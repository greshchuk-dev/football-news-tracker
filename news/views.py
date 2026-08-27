from django.shortcuts import render
from .models import NewsArticle, Team

def article_list(request):
    teams = Team.objects.all()
    selected_team_name = request.GET.get('team')
    
    articles = NewsArticle.objects.order_by('-published_at')
    if selected_team_name:
        articles = articles.filter(team__name=selected_team_name)
    return render(request, 'news/article_list.html', {
        'articles': articles, 
        'teams': teams,
        'selected_team_name': selected_team_name,
        })