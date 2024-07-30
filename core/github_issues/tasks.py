import os

import requests
from asgiref.sync import async_to_sync
from celery import shared_task
from client.models import Result, Client
from django.conf import settings
from django.contrib.auth.models import User
from telegram.ext import ApplicationBuilder
from telegram.ext import CallbackContext

from .models import Repository, Label
from bot import notify

telegram_bot = ApplicationBuilder().token(os.getenv('BOT_TOKEN')).build()


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
        Label.objects.update_or_create(
            repository=repository,
            name=label['name'],
            defaults={'color': label['color']}
        )


@shared_task()
def search_issues_task(repository_id, labels, user_id):

    repository = Repository.objects.get(id=repository_id)
    url = f"https://api.github.com/repos/{repository.owner}/{repository.name}/issues"
    params = {
        'labels': ','.join(labels),
        'page': 1,
    }
    message = f'Here what I found for you on {repository.owner}\'s {repository.name} repository.\n'
    message += '----------------------------------------------------------------------------------\n'
    response = requests.get(url, headers={'Authorization': f'Bearer {settings.AUTH_TOKEN}'}, params=params)
    issues = []
    while response.status_code == 200:
        new = response.json()
        if not new:
            break
        issues.extend(new)
        params['page'] += 1
        response = requests.get(url, headers={'Authorization': f'Bearer {settings.AUTH_TOKEN}'}, params=params)

    for issue in issues:
        tags = str()
        assignees = str()
        title = issue['title']
        html_url = issue['html_url']
        for assignee in issue['assignees']:
            assignees += assignee['login'] + ', '
        for label in issue['labels']:
            tags += label['name'] + ', '
        user = User.objects.get(id=user_id)
        Result.objects.update_or_create(
            title=title,
            html_url=html_url,
            assignees=assignees,
            labels=labels,
            client=Client.objects.get(user=user),
        )
        message += f'{title}: {html_url}'

    client = Client.objects.get(user_id=user_id)
    chat_id = client.telegram_id
    context = CallbackContext(telegram_bot)
    async_to_sync(notify)(context, message=message, chat_id=chat_id)
