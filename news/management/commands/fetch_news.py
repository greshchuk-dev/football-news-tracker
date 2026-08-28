from django.core.management.base import BaseCommand
from news.services import fetch_football_news
from news.models import NewsArticle, Team

class Command(BaseCommand):
    help = "Fetch latest football news and save new articles to the database"

    def handle(self, *args, **options):
        teams = Team.objects.all()
        new_count = 0

        for team in teams:
            articles = fetch_football_news(team.search_query)

            for article in articles:
                obj, created = NewsArticle.objects.get_or_create(
                    url=article['url'],
                    defaults={
                        'title': article['title'],
                        'author': article.get('author'),
                        'description': article.get('description'),
                        'url_to_image': article.get('urlToImage'),
                        'published_at': article['publishedAt'],
                        'content': article.get('content'),
                        'source_name': article['source']['name'],
                        'team': team,
                    }
                )
                if created:
                    new_count += 1

        self.stdout.write(self.style.SUCCESS(f"Saved {new_count} new articles"))