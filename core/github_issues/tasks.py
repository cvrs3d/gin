import requests
from celery import shared_task
from celery_singleton import Singleton
from django.conf import settings
from .models import Repository, Label


@shared_task(base=Singleton)
def fetch_labels_task(repository_id):
    repository = Repository.objects.get(id=repository_id)
    url = f"https://api.github.com/repos/{repository.owner}/{repository.name}/labels"
    response = requests.get(url, headers={'Authorization': f'Bearer {settings.AUTH_TOKEN}'})

    if response.status_code == 200:
        labels = response.json()
    else:
        labels = []

    for label in labels:
        Label.objects.update_or_create(
            repository=repository,
            name=label['name'],
            defaults={'color': label['color']}
        )


@shared_task(base=Singleton)
def search_issues_task(repository_id, labels):
    repository = Repository.objects.get(id=repository_id)
    url = f"https://api.github.com/repos/{repository.owner}/{repository.name}/labels"
    params = {
        'labels': ','.join(labels)
    }
    response = requests.get(url,headers={'Authorization':f'Bearer {settings.AUTH_TOKEN}'}, params=params)
    issues = response.json()
    print(issues)
