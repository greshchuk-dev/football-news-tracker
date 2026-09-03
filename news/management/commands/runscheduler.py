from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.management.base import BaseCommand
from django.core.management import call_command
import logging

logger = logging.getLogger(__name__)

def fetch_news_job():
    call_command('fetch_news')

class Command(BaseCommand):
    help = "Runs the APScheduler to periodically fetch football news"

    def handle(self, *args, **options):
        scheduler = BlockingScheduler()
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            fetch_news_job,
            trigger=IntervalTrigger(hours=2), 
            id="fetch_news_job",
            max_instances=1,
            replace_existing=True,
        )

        self.stdout.write(self.style.SUCCESS("Scheduler started. Press Ctrl+C to stop."))

        try:
            scheduler.start()
        except KeyboardInterrupt:
            scheduler.shutdown()
            self.stdout.write(self.style.SUCCESS("Scheduler stopped."))

