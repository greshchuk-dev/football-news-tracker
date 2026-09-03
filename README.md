# Football News Tracker

## Overview
A Django app that fetches and displays the latest news for a football team (currently Arsenal FC) using the NewsAPI. Articles are automatically filtered for relevance and saved to a database, avoiding duplicates.

## Features
- Fetches live football news from NewsAPI
- Filters results to a specific team using exact-phrase search and trusted sports domains
- Stores articles in a database, avoiding duplicates
- Displays a styled news feed
- Support multiple teams
- Automatically fetches news on a schedule using APScheduler (every 2 hours)

## Tech Stack
- Python / Django
- NewsAPI (external data source)
- SQLite (development database)

## Architecture
1. Fetch data from NewsAPI and filter for relevance
2. Save new articles to the Django database via a management command
3. Display articles through a Django view and template

## Setup
1. Clone the repo
2. Create and activate a virtual environment
3. `pip install -r requirements.txt`
4. Create a `.env` file with `NEWSAPI_KEY=your_key_here`
5. `python manage.py migrate`
6. `python manage.py createsuperuser` (optional, for admin access)
7. `python manage.py runserver`

## Fetching news
Run: `python manage.py fetch_news`
This could be automated in future with a scheduler like Celery or a cron job.

## Running the scheduler
To have news fetched automatically at a fixed interval, run:
```bash
python manage.py runscheduler
```
This starts a persistent process that fetches news every 2 hours (configurable in `news/management/commands/runscheduler.py`). Job execution history is visible in the Django admin under **Django Q Job Executions**. In production, this would typically run as a background service (e.g. via a process manager like `systemd` or `supervisor`) rather than in a terminal window.

## Possible future improvements
- Support multiple teams
- User accounts to follow favourite teams