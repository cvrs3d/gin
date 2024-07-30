from celery import shared_task
from .models import Result, Client
from datetime import timedelta
from  django.utils import timezone


@shared_task
def remove_old_results_task(client_id):
    old = timezone.now() - timedelta(hours=1)
    Result.objects.filter(client_id=client_id, created_at__lt=old).delete()
