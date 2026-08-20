from django.core.management.base import BaseCommand
from news.services import fetch_football_news
from news.models import NewsArticle

class Command(BaseCommand):
    help = "Fetch latest football news and save new articles to the database"

    def handle(self, *args, **options):
        team_name = "Arsenal FC"
        articles = fetch_football_news(team_name)

        new_count = 0
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
            }
        )
        if created:
            new_count += 1
           

        self.stdout.write(self.style.SUCCESS(f"Saved {new_count} new articles"))