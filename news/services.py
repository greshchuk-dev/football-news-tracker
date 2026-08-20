import requests
from django.conf import settings

def fetch_football_news(team_name):
    url = "https://newsapi.org/v2/everything"
    
    params = {
        "q": f'"{team_name}"',   # wraps the team name in quotes for exact phrase match
        "apiKey": settings.NEWSAPI_KEY,
        "language": "en",
        "sortBy": "publishedAt",
        "domains": "bbc.co.uk,skysports.com,theguardian.com,espn.com",
    }

    response = requests.get(url, params=params)
    data = response.json()
    articles = data["articles"]

    return articles
