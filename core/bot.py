import os

from django import setup
from django.apps import apps
from telegram import Update
from django.conf import settings
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

token = os.getenv('BOT_TOKEN')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Hello that\'s your user_id{update.message.from_user.id}, \nthat\'s your chat id{update.effective_chat.id}'
    )


async def notify(context: ContextTypes.context, message, chat_id):
    await context.bot.send_message(
        chat_id=chat_id,
        text=message
    )


if __name__ == '__main__':
    if not apps.ready:
        setup()
    application = ApplicationBuilder().token(token).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    application.run_polling()
