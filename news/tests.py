from django.test import TestCase
from .models import NewsArticle, Team
from unittest.mock import patch, MagicMock
from .services import fetch_football_news
from django.core.management import call_command
from io import StringIO

class NewsArticleModelTest(TestCase):
    def setUp(self):
        self.article = NewsArticle.objects.create(
            title="Arsenal win 3-0",
            url="https://www.example.com/article-1",
            published_at= "2026-08-20T10:00:00Z",
            source_name = "Test Source",
        )
    def test_string_representation(self):
        self.assertEqual(str(self.article), "Arsenal win 3-0")

    def test_article_created(self):
        self.assertEqual(NewsArticle.objects.count(), 1)
        
class ArticleListViewTest(TestCase):
    def setUp(self):
        NewsArticle.objects.create(
            title="Arsenal win 3-0",
            url="https://www.example.com/article-1",
            published_at= "2026-08-20T10:00:00Z",
            source_name = "Test Source",
        )

    def test_view_returns_200(self):
        response = self.client.get('/news/')
        self.assertEqual(response.status_code, 200)

    def test_view_shows_article_title(self):
        response = self.client.get('/news/')
        self.assertContains(response, "Arsenal win 3-0")

    def test_view_filters_by_team(self):
        arsenal = Team.objects.create(name="Arsenal FC", search_query="Arsenal FC")
        chelsea = Team.objects.create(name="Chelsea FC", search_query="Chelsea FC")
        NewsArticle.objects.create(
            title="Arsenal win 3-0",
            url="https://www.example.com/article-arsenal",
            published_at= "2026-08-20T10:00:00Z",
            source_name = "Test Source",
            team=arsenal
        )
        NewsArticle.objects.create(
            title="Chelsea win 2-1",
            url="https://www.example.com/article-chelsea",
            published_at= "2026-08-21T10:00:00Z",
            source_name = "Test Source",
            team=chelsea
        )

        response = self.client.get('/news/', {'team': 'Arsenal FC'})

        self.assertContains(response, "Arsenal win 3-0")
        self.assertNotContains(response, "Chelsea win 2-1")

class FetchFootballNewsTest(TestCase):
    @patch('news.services.requests.get')
    def test_fetch_returns_articles(self, mock_get):
        # Build a fake response object, representing the actual API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "ok",
            "totalResults": 1,
            "articles": [
                {
                    "source": {"id": None, "name": "Test Source"},
                    "author": "Test Author",
                    "title": "Fake Arsenal Article",
                    "description": "A fake description",
                    "url": "https://www.example.com/fake-article",
                    "publishedAt": "2026-08-20T10:00:00Z",
                    "content": "Fake content"
                }
            ],
        }
        mock_get.return_value = mock_response

        articles = fetch_football_news("Arsenal FC")

        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0]['title'], "Fake Arsenal Article")

class FetchNewsCommandTest(TestCase):
    @patch('news.services.requests.get')
    def test_command_saves_new_article(self, mock_get):
        Team.objects.create(name="Arsenal FC", search_query="Arsenal FC")
        # Build a fake response object, representing the actual API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "ok",
            "articles": [
                {
                    "source": {"id": None, "name": "Test Source"},
                    "author": "Test Author",
                    "title": "Fake Arsenal Article",
                    "description": "A fake description",
                    "url": "https://www.example.com/fake-article",
                    "urlToImage": None,
                    "publishedAt": "2026-08-20T10:00:00Z",
                    "content": "Fake content"
                }
            ]
        }
        mock_get.return_value = mock_response

        out = StringIO()
        call_command('fetch_news', stdout=out)

        self.assertEqual(NewsArticle.objects.count(), 1)
        self.assertIn("Saved 1 new articles", out.getvalue())

    @patch('news.services.requests.get')
    def test_command_skips_duplicate(self, mock_get):
        Team.objects.create(name="Arsenal FC", search_query="Arsenal FC")
        # Precreate an article with the same URL the moke will fetch
        NewsArticle.objects.create(
            title="Existing Article",
            url="https://www.example.com/fake-article",
            published_at= "2026-08-20T10:00:00Z",
            source_name = "Test Source",
        )

        # Build a fake response object, representing the actual API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "ok",
            "articles": [
                {
                    "source": {"id": None, "name": "Test Source"},
                    "author": "Test Author",
                    "title": "Fake Arsenal Article", 
                    "description": "A fake description",
                    "url": "https://www.example.com/fake-article", 
                    "urlToImage": None,
                    "publishedAt": "2026-08-20T10:00:00Z",
                    "content": "Fake content"
                }
            ]
        }
        mock_get.return_value = mock_response

        out = StringIO()
        call_command('fetch_news', stdout=out)

        self.assertEqual(NewsArticle.objects.count(), 1)  # Should still be 1, no new article added
        self.assertIn("Saved 0 new articles", out.getvalue())