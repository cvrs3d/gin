from celery import shared_task
from django.conf import settings
import requests
from .models import Repository, Label
import logging

logger = logging.getLogger(__name__)


# @shared_task()
# def fetch_labels_task(repository_id):
#     print(f"Processing repository with ID {repository_id}")

@shared_task
def add(x, y):
    print(x + y)


@shared_task()
def fetch_labels_task(repository_id):
    repository = Repository.objects.get(id=repository_id)
    params = {
        'page': 1,
    }
    url = f"https://api.github.com/repos/{repository.owner}/{repository.name}/labels"
    labels = []
    response = requests.get(url, headers={'Authorization': f'Bearer {settings.AUTH_TOKEN}'}, params=params)

    while response.status_code == 200:
        new = response.json()
        if not new:
            break
        labels.extend(new)
        params['page'] += 1
        response = requests.get(url, headers={'Authorization': f'Bearer {settings.AUTH_TOKEN}'}, params=params)

    for label in labels:
        print(label['name'])
        Label.objects.update_or_create(
            repository=repository,
            name=label['name'],
            defaults={'color': label['color']}
        )


@shared_task()
def search_issues_task(repository_id, labels):
    repository = Repository.objects.get(id=repository_id)
    url = f"https://api.github.com/repos/{repository.owner}/{repository.name}/labels"
    params = {
        'labels': ','.join(labels)
    }
    response = requests.get(url, headers={'Authorization': f'Bearer {settings.AUTH_TOKEN}'}, params=params)
    issues = response.json()
    print(issues)
