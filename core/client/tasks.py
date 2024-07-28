from celery import shared_task
from .models import Result, Client
from datetime import timedelta
from  django.utils import timezone


@shared_task
def remove_old_results_task(client_id):
    twelve_hours_old = timezone.now() - timedelta(hours=12)
    Result.objects.filter(client_id=client_id, created_at__lt=twelve_hours_old).delete()
